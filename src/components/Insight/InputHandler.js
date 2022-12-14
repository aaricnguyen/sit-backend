/* eslint-disable import/prefer-default-export */
import { INSIGHT_CASE } from '../../constants';
import { getTotalConfigs } from '../../services/CustomerService';
import * as RedisService from '../../services/RedisService';

export const parseInsightInput = async (key) => {
  // const externalCustomers = (await RedisService.get('externalCustomers')) || [];
  const internalCustomers = (await RedisService.get('internalCustomers')) || [];
  const categories = (await RedisService.get('categories')) || [];
  const totalConfig = getTotalConfigs(categories);
  const splitData = key.split(' ');
  let result = {};

  for (let index = 0; index < splitData.length; index += 1) {
    const item = splitData[index];
    if (splitData.length === 1) {
      const customer = internalCustomers.find(
        (intCus) => intCus.cust_id === item,
      );
      if (customer) {
        result = {
          type: INSIGHT_CASE.INSIGHT_CASE_1,
          data: customer.cust_id,
        };
        break;
      }
    }
    if (index !== 0) {
      const prevItem = splitData[index - 1];
      const nextItem = splitData[index + 1];
      // case 2
      if (item === '+') {
        let feature = totalConfig.find((f) => f === prevItem);
        let customer = internalCustomers.find(
          (intCus) => intCus.cust_id === nextItem,
        );

        if (!feature) {
          feature = totalConfig.find((f) => f === nextItem);
          customer = internalCustomers.find(
            (intCus) => intCus.cust_id === prevItem,
          );
        }
        if (feature && customer) {
          result = {
            type: INSIGHT_CASE.INSIGHT_CASE_2,
            data: {
              feature: prevItem,
              customer: nextItem,
            },
          };
        }
      }
    }
  }
  return result;
};
