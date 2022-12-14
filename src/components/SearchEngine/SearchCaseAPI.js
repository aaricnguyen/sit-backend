import { difference, intersection } from 'lodash';
import { OPERATOR } from '../../constants/index';
import {
  getConfigDataCombine,
  getExternalCustomerSummaryInfo,
  getInternalCustomerSummaryInfo,
  getScaleDataCombine,
  getTotalConfigs,
} from '../../services/CustomerService';
import * as RedisService from '../../services/RedisService';

/**
 * Case 1
 * exter customer id, internal finance, education
 */
export const getCustomerData = async (customerId) => {
  const externalCustomers = (await RedisService.get('externalCustomers')) || [];
  const internalCustomers = (await RedisService.get('internalCustomers')) || [];

  let customer = internalCustomers.find((item) => item.cust_id === customerId);
  if (customer) {
    const getDataCustomer = await getInternalCustomerSummaryInfo(customer);
    const { cust_id, totalConfig, totalExternalCustomerMatch } =
      getDataCustomer;
    return {
      cust_id,
      totalConfig,
      totalExternalCustomerMatch,
    };
  }
  customer = externalCustomers.find((item) => item.cust_id === customerId);

  const getDataCombine = await getExternalCustomerSummaryInfo(customer);
  const { dataCombine, totalConfig } = getDataCombine;
  return {
    dataCombine,
    totalConfig,
  };
};

/**
 * Case 2
 * one single feature or multiple features f1 and f2 and f3
 * result: 100/150 (80%) external customers has f1, f2, f3
 *   both finance and education covered f1,f2,f3
 *   f1 is covered by finance and f2,f3 covered by education
 */
export const getFeatureData = async (features = []) => {
  const externalCustomers = (await RedisService.get('externalCustomers')) || [];
  const externalCustomerHasFeatures = externalCustomers.filter(
    (item) => difference(features, getTotalConfigs(item)).length === 0,
  );
  const getDataCombine = await getConfigDataCombine(features);
  const { dataCombine, totalConfig } = getDataCombine;
  return {
    totalExternalCustomer: externalCustomers.length,
    totalExternalCustomerHasFeatures: externalCustomerHasFeatures.length,
    dataCombine,
    totalConfig,
  };
};

/**
 * Case 3
 * single/multiple features + customer id(both external and internal)
 * result: if this feature/combination is covered in the customer id or not
 */
export const getFeatureAndCustomerCombination = async ({
  features,
  customer: customerId,
}) => {
  const externalCustomers = (await RedisService.get('externalCustomers')) || [];
  const internalCustomers = (await RedisService.get('internalCustomers')) || [];

  let customer = internalCustomers.find((item) => item.cust_id === customerId);
  if (customer) {
    customer = externalCustomers.find((item) => item.cust_id === customerId);
  }

  const totalConfig = getTotalConfigs(customer);
  const check = difference(features, totalConfig).length;
  return {
    features,
    customer: customerId,
    isCovered: check !== 0,
  };
};

/**
 * Case 4
 *  !(f1 and f2)
 * result: f1 and f2 are absent in 50/150(30%) of external customers
 */
export const getNegativeFeatureData = async (features = []) => {
  const externalCustomers = (await RedisService.get('externalCustomers')) || [];
  const externalCustomerNotHasFeatures = externalCustomers.filter(
    (item) => difference(features, getTotalConfigs(item)).length !== 0,
  );
  const getDataCombine = await getConfigDataCombine(features);
  const { dataCombine, totalConfig } = getDataCombine;
  return {
    totalExternalCustomer: externalCustomers.length,
    totalExternalCustomerNotHasFeatures: externalCustomerNotHasFeatures.length,
    dataCombine,
    totalConfig,
  };
};

/**
 * Case 5
 *  f1 xor f2 (1/0, 0/1)
 *  result like 2.
 */
export const getXorFeatureData = async (features = []) => {
  const externalCustomers = (await RedisService.get('externalCustomers')) || [];
  const externalCustomerHasFeatures = features.map((feature) => {
    const xorFeatures = difference(features, [feature]);
    const value = externalCustomers.filter((item) => {
      const totalConfig = getTotalConfigs(item);
      return (
        totalConfig.includes(feature) &&
        intersection(totalConfig, xorFeatures).length === 0
      );
    }).length;

    return {
      feature,
      value,
    };
  });

  const getDataCombine = await getConfigDataCombine(features);
  const { dataCombine, totalConfig } = getDataCombine;
  return {
    totalExternalCustomer: externalCustomers.length,
    externalCustomerHasFeatures,
    dataCombine,
    totalConfig,
  };
};

/**
 * Case 6
 * scale search (no. of dot1x interfaces > 100 ) single
 * or combination( scale f1 >100 and scale f2 > 50)
 * r. like 2
 * @input : [{name:f3, value:100, operator: '>'}]
 */
export const getScaleSearchData = async (conditions = []) => {
  const externalCustomers = (await RedisService.get('externalCustomers')) || [];
  const externalCustomerConditionSatisfy = externalCustomers.filter(
    (customer) => {
      const { featureCounts } = customer;
      for (let i = 0; i < conditions.length; i += 1) {
        const condition = conditions[i];
        const { name, value, operator } = condition;
        if (!featureCounts[name]) {
          return false;
        }
        switch (operator) {
          case OPERATOR.GREATER:
            if (featureCounts[name] <= value) return false;
            break;
          case OPERATOR.GREATER_OR_EQUAL:
            if (featureCounts[name] < value) return false;
            break;
          case OPERATOR.LESS:
            if (featureCounts[name] >= value) return false;
            break;
          case OPERATOR.LESS_OR_EQUAL:
            if (featureCounts[name] > value) return false;
            break;
          case OPERATOR.NOT_EQUAL:
            if (featureCounts[name] === value) return false;
            break;
          case OPERATOR.EQUAL:
            if (featureCounts[name] !== value) return false;
            break;
          default:
            return false;
        }
      }
      return true;
    },
  );

  const getDataCombine = await getScaleDataCombine(conditions);
  const { dataCombine } = getDataCombine;
  return {
    totalExternalCustomer: externalCustomers.length,
    externalCustomerConditionSatisfy: externalCustomerConditionSatisfy.length,
    dataCombine,
    conditions,
  };
};

/**
 * Case 7
 * feature count + feature
 * result: if this feature/combination is covered in the customer id or not
 */
export const getFeatureAndFeatureCount = async ({
  features = [],
  conditions = [],
}) => {
  const externalCustomers = (await RedisService.get('externalCustomers')) || [];
  let externalCustomerConditionSatisfy = externalCustomers.filter(
    (customer) => {
      const { featureCounts } = customer;
      const totalConfig = getTotalConfigs(customer);
      // this customer don't have the features
      if (difference(features, totalConfig).length !== 0) {
        return false;
      }
      for (let i = 0; i < conditions.length; i += 1) {
        const condition = conditions[i];
        const { name, value, operator } = condition;
        if (!featureCounts[name]) {
          return false;
        }
        switch (operator) {
          case OPERATOR.GREATER:
            if (featureCounts[name] <= value) return false;
            break;
          case OPERATOR.GREATER_OR_EQUAL:
            if (featureCounts[name] < value) return false;
            break;
          case OPERATOR.LESS:
            if (featureCounts[name] >= value) return false;
            break;
          case OPERATOR.LESS_OR_EQUAL:
            if (featureCounts[name] > value) return false;
            break;
          case OPERATOR.NOT_EQUAL:
            if (featureCounts[name] === value) return false;
            break;
          case OPERATOR.EQUAL:
            if (featureCounts[name] !== value) return false;
            break;
          default:
            return false;
        }
      }
      return true;
    },
  );

  const getDataCombine = await getScaleDataCombine(conditions);
  const { dataCombine } = getDataCombine;
  return {
    totalExternalCustomer: externalCustomers.length,
    externalCustomerConditionSatisfy: externalCustomerConditionSatisfy.length,
    dataCombine,
    conditions,
  };
};
