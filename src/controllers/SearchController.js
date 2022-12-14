/* eslint-disable no-restricted-syntax */
import { concat } from 'lodash';
import { parseInput } from '../components/SearchEngine/InputHandler';
import ManageSearchAPIs from '../components/SearchEngine/ManageSearchAPIs';
import { getTotalConfigs } from '../services/CustomerService';
import * as RedisService from '../services/RedisService';
import { responseError, responseSuccess } from '../services/Response';

const checkBrackets = (str) => {
  const stack = [];
  for (const character of str) {
    if (character === '(') {
      stack.push(character);
    }
    if (character === ')') stack.pop();
  }
  return !stack.length;
};

const queryOperator = ['and', 'xor'];
const comparisonOperator = ['<', '>', '!=', '>=', '<='];

export const searchSuggestions = async (req, res) => {
  const { q } = req.query;

  const keywordSplit = q.split(' ');
  const keyword = keywordSplit[keywordSplit.length - 1];
  const isBracketed = checkBrackets(q);
  const checkData = keywordSplit[keywordSplit.length - 2];

  let externalCustomers = (await RedisService.get('externalCustomers')) || [];
  let internalCustomers = (await RedisService.get('internalCustomers')) || [];

  if (
    !concat(queryOperator, comparisonOperator, ['+']).includes(checkData)
    && keywordSplit.length > 1
  ) {
    if (
      externalCustomers.find((ext) => ext.cust_id === checkData)
      || internalCustomers.find((ext) => ext.cust_id === checkData)
    ) {
      return res.json(
        responseSuccess({
          data: [
            `${keywordSplit.slice(0, keywordSplit.length - 1).join(' ')} +`,
          ],
        }),
      );
    }
    const data = [...queryOperator]
      .filter((item) => item.includes(keyword))
      .map(
        (item) => `${keywordSplit.slice(0, keywordSplit.length - 1).join(' ')} ${item}`,
      );

    return res.json(
      responseSuccess({
        data,
      }),
    );
  }

  const categories = (await RedisService.get('categories')) || [];
  let { featureCounts = [] } = categories;

  let totalConfigs = getTotalConfigs(categories);

  totalConfigs = totalConfigs.filter((item) => item.startsWith(keyword)) || [];

  featureCounts = featureCounts.filter((item) => item.startsWith(keyword));

  externalCustomers = externalCustomers
    .filter((item) => item.cust_id.startsWith(keyword))
    .map((i) => i.cust_id);

  internalCustomers = internalCustomers
    .filter(
      (item) => item.cust_id.startsWith(keyword) && item.cust_id !== 'others',
    )
    .map((i) => i.cust_id);

  let data = [
    ...totalConfigs,
    ...featureCounts,
    ...externalCustomers,
    ...internalCustomers,
  ];

  if (keywordSplit.length <= 1) {
    data = [
      ...externalCustomers,
      ...internalCustomers,
      ...totalConfigs,
      ...featureCounts,
    ];
  }
  data = data.slice(0, 5).map((item) => {
    const newItem = isBracketed ? item : `${item})`;
    return `${newItem}`;
  });

  res.json(
    responseSuccess({
      data,
    }),
  );
};

export const getSearchDataDetail = async (req, res) => {
  const { type, data } = req.query;
  try {
    const result = await ManageSearchAPIs(type, JSON.parse(data));
    res.json(
      responseSuccess({
        data: result,
      }),
    );
  } catch (err) {
    return res.json(
      responseError({
        message: 'Query data is not valid',
        data: err.message,
      }),
    );
  }
};

export const search = async (req, res) => {
  const externalCustomers = (await RedisService.get('externalCustomers')) || [];
  const internalCustomers = (await RedisService.get('internalCustomers')) || [];
  const { q } = req.query;
  const data = await parseInput(externalCustomers, internalCustomers, q);
  res.json(
    responseSuccess({
      data,
    }),
  );
};
