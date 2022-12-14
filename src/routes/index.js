import express from 'express';
import * as CustomerController from '../controllers/CustomerController';
import * as SearchController from '../controllers/SearchController';
import * as InsightController from '../controllers/InsightController';
import * as UploadService from '../services/UploadService';
import * as UserController from '../controllers/UserController';
import { featurePolicy } from 'helmet';

const router = express.Router();

router.get('/update', CustomerController.updateV2);
router.get('/overview', CustomerController.getOverview);

router.get('/chart', CustomerController.getChartData);
router.get('/scale-chart', CustomerController.getScaleChartData);

router.get(
  '/customer-compare-by-id-chart',
  CustomerController.getExternalCustomerCompareById,
);

router.get(
  '/customer-feature-config-by-segment',
  CustomerController.getExternalFeatureConfigBySegment2,
);
router.get(
  '/global-top-feature-25',
  CustomerController.getGlobalTop25,
);

router.get(
  '/customer-feature-count-by-segment',
  CustomerController.getExternalFeatureCountBySegment,
);

router.get(
  '/get-external-summary-info',
  CustomerController.getExternalSummaryInfo,
);

router.post(
  '/upload',
  UploadService.setUploader,
  UploadService.handleZipFie,
  CustomerController.uploadConfigFile,
);

router.post(
  '/upload-template',
  UploadService.setUploaderTemplate,
  InsightController.uploadTemplateFile,
);

router.get('/update-template', InsightController.updatedTemplateFile);

// ====================== search routes ======================
router.get('/search', SearchController.search);
router.get('/search-suggestions', SearchController.searchSuggestions);
router.get('/get-search-data-detail', SearchController.getSearchDataDetail);

// ====================== Insight ======================
router.get('/insights', InsightController.getAll);

// ====================== internal customer ======================
router.get('/internal-customers', CustomerController.getListInternalCustomer);

// ====================== user ======================
router.get('/get-user', UserController.getUser);
router.get('/add-user', UserController.addUser);
router.get('/update-user', UserController.updateUser);
router.get('/get-total-visit-count', UserController.getTotalVisitCount);

export default router;
