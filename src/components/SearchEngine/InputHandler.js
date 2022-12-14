/* eslint-disable import/prefer-default-export */
import { OPERATOR, SEARCH_CASE } from '../../constants';
import { getTotalConfigs } from '../../services/CustomerService';
import * as RedisService from '../../services/RedisService';

const getFeatureWithoutBracket = (item) => {
  const result = item.replace('!(', '').replace('!', '').replace(')', '');
  return result;
};

const getFeatures = (totalConfig, arrStr) => {
  let featureList = [];
  if (arrStr.length === 1) {
    if (totalConfig.includes(arrStr[0])) {
      featureList.push(arrStr[0]);
    }
  }

  for (let index = 0; index < arrStr.length; index += 1) {
    const item = arrStr[index];

    if (index !== 0) {
      const prevItem = arrStr[index - 1];
      const nextItem = arrStr[index + 1];
      if (item === 'and') {
        if (totalConfig.includes(prevItem)) {
          featureList.push(prevItem);
        }
        if (totalConfig.includes(nextItem)) {
          featureList.push(nextItem);
        }
        featureList = [...new Set(featureList)];
      }
    }
  }

  return featureList;
};

export const parseInput = async (
  externalCustomers,
  internalCustomers,
  keyword,
) => {
  const categories = (await RedisService.get('categories')) || [];
  const { featureCounts = [] } = categories;
  const splitData = keyword.split(' ');
  const totalConfig = getTotalConfigs(categories);
  let resultList = [];
  const resultCase1 = [];
  let featureList = [];
  let featureXorList = [];
  let featureNegativeList = [];

  const dataCase2 = {
    type: SEARCH_CASE.SEARCH_CASE_2,
    data: [],
  };
  const dataCase3 = {
    type: SEARCH_CASE.SEARCH_CASE_3,
    data: {},
  };
  const dataCase4 = {
    type: SEARCH_CASE.SEARCH_CASE_4,
    data: [],
  };
  const dataCase5 = {
    type: SEARCH_CASE.SEARCH_CASE_5,
    data: [],
  };
  const dataCase6 = {
    type: SEARCH_CASE.SEARCH_CASE_6,
    data: [],
  };
  const dataCase7 = {
    type: SEARCH_CASE.SEARCH_CASE_7,
    data: {},
  };
  const bracketNegatives = [];

  for (let index = 0; index < splitData.length; index += 1) {
    const item = splitData[index];
    if (item.includes('!(')) {
      bracketNegatives.push(item);
    }
    if (splitData.length === 1) {
      externalCustomers
        .filter((extCus) => extCus.cust_id.indexOf(item) === 0)
        .forEach((extCus) => {
          resultCase1.push({
            type: SEARCH_CASE.SEARCH_CASE_1,
            data: extCus.cust_id,
          });
        });
      internalCustomers
        .filter((intCus) => intCus.cust_id.indexOf(item) === 0)
        .forEach((intCus) => {
          resultCase1.push({
            type: SEARCH_CASE.SEARCH_CASE_1,
            data: intCus.cust_id,
          });
        });
    }

    if (splitData.length === 1) {
      if (totalConfig.includes(getFeatureWithoutBracket(item))) {
        if (item.includes('!')) {
          featureNegativeList.push(getFeatureWithoutBracket(item));
        } else featureList.push(item);
      }
    }

    if (index !== 0) {
      const prevItem = splitData[index - 1];
      const nextItem = splitData[index + 1];
      if (Object.values(OPERATOR).includes(item)) {
        const value = Number.isNaN(parseFloat(nextItem))
          ? 0
          : parseFloat(nextItem);

        const feature = featureCounts.find(
          (featureCount) => featureCount.indexOf(prevItem) > -1,
        );
        if (feature) {
          dataCase6.data.push({
            name: feature,
            value,
            operator: item,
          });
        }
      } else if (item === 'and') {
        if (bracketNegatives.length > 0) {
          if (item.includes(')')) {
            bracketNegatives.pop();
          }
          if (totalConfig.includes(getFeatureWithoutBracket(prevItem))) {
            featureNegativeList.push(getFeatureWithoutBracket(prevItem));
          }
          if (totalConfig.includes(getFeatureWithoutBracket(nextItem))) {
            featureNegativeList.push(getFeatureWithoutBracket(nextItem));
          }
          featureNegativeList = [...new Set(featureNegativeList)];
        }
        if (totalConfig.includes(prevItem)) {
          featureList.push(prevItem);
        }
        if (totalConfig.includes(nextItem)) {
          featureList.push(nextItem);
        }
        featureList = [...new Set(featureList)];
      } else if (item === 'xor') {
        if (totalConfig.includes(prevItem)) {
          featureXorList.push(prevItem);
        }
        if (totalConfig.includes(nextItem)) {
          featureXorList.push(nextItem);
        }
        featureXorList = [...new Set(featureXorList)];
      } else if (item === '+') {
        let customer = externalCustomers.find(
          (extCus) => extCus.cust_id === prevItem,
        );
        if (!customer) {
          customer = internalCustomers.find(
            (intCus) => intCus.cust_id === prevItem,
          );
        }
        if (customer) {
          dataCase3.data.customer = customer.cust_id;
          dataCase3.data.features = getFeatures(
            totalConfig,
            splitData.slice(index + 1),
          );
        } else {
          customer = externalCustomers.find(
            (extCus) => extCus.cust_id === nextItem,
          );
          if (!customer) {
            customer = internalCustomers.find(
              (intCus) => intCus.cust_id === nextItem,
            );
          }
          if (customer) {
            dataCase3.data.customer = customer.cust_id;
            dataCase3.data.features = getFeatures(
              totalConfig,
              splitData.slice(0, index),
            );
          }
        }
      }
    }
  }

  dataCase2.data = featureList;
  dataCase4.data = featureNegativeList;
  dataCase5.data = featureXorList;

  if (dataCase6.data.length !== 0 && dataCase2.data.length !== 0) {
    dataCase7.data.features = dataCase2.data;
    dataCase7.data.conditions = dataCase6.data;
  }

  resultList = [
    dataCase7,
    dataCase6,
    dataCase3,
    dataCase4,
    dataCase5,
    dataCase2,
    ...resultCase1.sort((a, b) => a.data.length - b.data.length),
  ];

  // remove duplicated and no data
  resultList = [
    ...new Set(
      resultList
        .filter((item) => Object.keys(item.data).length > 0)
        .map((i) => JSON.stringify(i)),
    ),
  ].map((i) => JSON.parse(i));
  return resultList;
};
