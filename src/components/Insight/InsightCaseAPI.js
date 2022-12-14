import { getTotalConfigs } from '../../services/CustomerService';
import * as RedisService from '../../services/RedisService';

/**
 * Insight Case 1
 * % of internal customers.
 */
export const getValueOfInternalCustomer = async (customerId) => {
  const internalCustomers = (await RedisService.get('internalCustomers')) || [];
  const externalCustomers = (await RedisService.get('externalCustomers')) || [];
  const internalCustomer = internalCustomers.find(
    (item) => item.cust_id === customerId,
  );

  let value = 0;
  if (internalCustomer) {
    value = Number(
      parseFloat(
        (internalCustomer.sameConfigs.length / externalCustomers.length) * 100,
      ).toFixed(2),
    );
  }

  return value;
};

/**
 * Insight Case 2
 * feature + customer
 */
export const getValueOfFeatureOfCustomer = async ({
  customer: customerId = '',
  feature = '',
}) => {
  const externalCustomers = (await RedisService.get('externalCustomers')) || [];
  const internalCustomers = (await RedisService.get('internalCustomers')) || [];
  const internalCustomer =
    internalCustomers.find((item) => item.cust_id === customerId) || {};

  const { sameConfigs = [] } = internalCustomer;
  let value = 0;
  let count = 0;
  sameConfigs.forEach((item) => {
    const externalCustomer = externalCustomers.find(
      (cus) => cus.cust_id === item.cust_id,
    );
    if (externalCustomer) {
      const totalConfig = getTotalConfigs(externalCustomer);
      if (totalConfig.includes(feature)) {
        count += 1;
      }
    }
  });

  if (sameConfigs.length > 0) {
    value = Number(parseFloat((count / sameConfigs.length) * 100).toFixed(2));
  }

  return value;
};
