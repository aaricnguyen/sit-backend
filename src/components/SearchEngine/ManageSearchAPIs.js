import { SEARCH_CASE } from '../../constants';
import {
  getCustomerData,
  getFeatureAndCustomerCombination,
  getFeatureAndFeatureCount,
  getFeatureData,
  getNegativeFeatureData,
  getScaleSearchData,
  getXorFeatureData,
} from './SearchCaseAPI';

const matchSearchCase = async (type, dataQuery) => {
  let data = dataQuery;
  let result = {};
  switch (type) {
    case SEARCH_CASE.SEARCH_CASE_1:
      result = await getCustomerData(data);
      break;
    case SEARCH_CASE.SEARCH_CASE_2:
      if (typeof data === 'string') data = [data];
      result = await getFeatureData(data);
      break;
    case SEARCH_CASE.SEARCH_CASE_3:
      result = await getFeatureAndCustomerCombination(data);
      break;
    case SEARCH_CASE.SEARCH_CASE_4:
      result = await getNegativeFeatureData(data);
      break;
    case SEARCH_CASE.SEARCH_CASE_5:
      result = await getXorFeatureData(data);
      break;
    case SEARCH_CASE.SEARCH_CASE_6:
      result = await getScaleSearchData(data);
      break;
    case SEARCH_CASE.SEARCH_CASE_7:
      result = await getFeatureAndFeatureCount(data);
      break;
    default:
      break;
  }

  return {
    type,
    data,
    result,
  };
};
export default matchSearchCase;
