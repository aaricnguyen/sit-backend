import { INSIGHT_CASE } from '../../constants';
import {
  getValueOfFeatureOfCustomer,
  getValueOfInternalCustomer,
} from './InsightCaseAPI';

const matchInsightCase = async (type, dataQuery) => {
  let result = 0;
  switch (type) {
    case INSIGHT_CASE.INSIGHT_CASE_1:
      result = await getValueOfInternalCustomer(dataQuery);
      break;
    case INSIGHT_CASE.INSIGHT_CASE_2:
      result = await getValueOfFeatureOfCustomer(dataQuery);
      break;
    default:
      result = 0;
      break;
  }

  return {
    type,
    dataQuery,
    result,
  };
};
export default matchInsightCase;
