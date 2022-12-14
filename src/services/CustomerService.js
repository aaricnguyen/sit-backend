import { cloneDeep, difference, differenceBy, forEach, intersection, isNaN } from 'lodash';
import {
  CATEGORIES,
  COVERED,
  COVERED_BY_COMBINATION,
  NOT_COVERED,
  OPERATOR,
  INTERNAL_CUST_SEGMENT,
} from '../constants/index';
import * as RedisService from './RedisService';

export const getSqlQueryUniqueCustomerData = ({arrQueryUnique})=>{
  let {features = [],featureCounts = []} = arrQueryUnique

  let arrcust_wt = [
    'retailwt',
    'govtwt',
    'healthwt',
    'ngewt',
    'educationwt',
    'financewt',
    'pewt',
    'ngevpnwt',
    'sdawt',
    'techsupport_sw_type',
    'cust_segment'
  ]
  arrcust_wt = arrcust_wt.map(item=>`max(${item}) as ${item}`)
  features = features.map(item=>`max(${item}) as ${item}`)
  featureCounts = featureCounts.map(item=>`SUM(${item}) as ${item}`)

  const sqlQueryUniqueCustomerData = `SELECT cust_id, ${arrcust_wt.join(',')}, ${featureCounts.join(',')}, ${features.join(',')} FROM custConfigDB.customerData GROUP BY cust_id`;
  return sqlQueryUniqueCustomerData
}
export const getCategoriesV2 = (results = []) => {
  const categories = {}
  const categoriesField = {}
  const arrQueryUnique = {
    featureCounts:[],
    features:[],
  }

  if (results.length === 0) return {};
  categories.featureCounts = [];
  forEach(CATEGORIES, ({ value }) => {
    categories[value] = [];
  });

  results.forEach((key) => {
    const keyArr = key.split('_');
    if (
      keyArr.length === 2 ||
      (keyArr.length === 3 && ['platform', 'misc'].includes(keyArr[0]))
    ) {
      const category = CATEGORIES.find(
        (categoryItem) => keyArr[0].indexOf(categoryItem.key) === 0,
      );
      if (category) {
        let feature = keyArr[1];
        if (keyArr[2]) {
          feature = `${keyArr[1]}_${keyArr[2]}`;
        }
        if (
          ['evpn', 'l3', 'l2'].includes(category.key) &&
          ['bgp', 'udld'].includes(keyArr[1])
        ) {
          // l3_udld, l2_udld, l3_bgp, evpn_bgp
          feature = `${category.key}_${feature}`;
        }
         categoriesField[key] =  category.value
        categories[category.value].push(feature);
        arrQueryUnique.features.push(key)
      }
    }

    if (keyArr[keyArr.length - 1] === 'count' || key === 'mac') {
      categoriesField[key] =  'featureCounts'
      categories.featureCounts.push(key);
      arrQueryUnique.featureCounts.push(key)

    }
  });

  return {categories,categoriesField,arrQueryUnique};
};
export const getMatchDataV2 = async ({internalCustomers, cust_segment_externalCustomers,cust_segment_internalCustomers,internalCustomersObj,categories}) => {
  // let sameCustomerIds = new Set();
  forEach(internalCustomers, (internalConfig, key) => {
    const totalInternalConfig = internalCustomersObj[internalConfig.cust_id].totalConfig;
    internalCustomers[key].sameConfigs = [];

    const listCust_segment_externalCustomers = cust_segment_externalCustomers[internalConfig.cust_segment] || []
    const intersectionDataObj = {}
    totalInternalConfig.forEach(item=>{
      intersectionDataObj[item] = 1
    })

    listCust_segment_externalCustomers.forEach(item=>{
      const {totalConfig : totalExternalConfig = [],cust_id} = item;
      const totalExternalConfigUnieq = totalExternalConfig
      let intersection = 0
      totalExternalConfigUnieq.forEach(item=>{
        if(intersectionDataObj[item]){
          intersection++
        }
      })
      const samePercent = Number(
        parseFloat(
          (intersection / totalExternalConfig.length) * 100,
        ).toFixed(2),
      );

      internalCustomers[key].sameConfigs.push({
        cust_id,
        value: samePercent,
      });
    })
  });
    const othersConfig = { cust_id: 'others', sameConfigs: [] };
  internalCustomers.push(othersConfig);

  // const categories = (await RedisService.get('categories')) || [];

  forEach(categories, (value, key) => {
    othersConfig[key] = value;
  });
  const listOthersConfig = differenceBy(Object.keys(cust_segment_externalCustomers),Object.keys(cust_segment_internalCustomers))
  listOthersConfig.forEach((cust_segment)=>{
    cust_segment_externalCustomers[cust_segment].forEach((item)=>{
      const {totalConfig : totalExternalConfig = [],cust_id} = item;

      othersConfig.sameConfigs.push({
        cust_id,
        value: totalExternalConfig.length,
      });
    })
  })
};
const getCategories = (results = [], categories = {}) => {
  if (results.length === 0) return {};
  categories.featureCounts = [];
  forEach(CATEGORIES, ({ value }) => {
    categories[value] = [];
  });

  forEach(results[0], (_, key) => {
    const keyArr = key.split('_');
    if (
      keyArr.length === 2 ||
      (keyArr.length === 3 && ['platform', 'misc'].includes(keyArr[0]))
    ) {
      const category = CATEGORIES.find(
        (categoryItem) => keyArr[0].indexOf(categoryItem.key) === 0,
      );
      if (category) {
        let feature = keyArr[1];
        if (keyArr[2]) {
          feature = `${keyArr[1]}_${keyArr[2]}`;
        }
        if (
          ['evpn', 'l3', 'l2'].includes(category.key) &&
          ['bgp', 'udld'].includes(keyArr[1])
        ) {
          // l3_udld, l2_udld, l3_bgp, evpn_bgp
          feature = `${category.key}_${feature}`;
        }
        categories[category.value].push(feature);
      }
    }

    if (keyArr[keyArr.length - 1] === 'count' || key === 'mac') {
      categories.featureCounts.push(key);
    }
  });

  return categories;
};

const convertConfig = (config) => {
  const newConfig = {
    cust_id: config.cust_id,
    cust_segment: config.cust_segment,
    featureCounts: {},
    cust_wt: {},
    techsupport_sw_type : String(config.techsupport_sw_type),
  };


  forEach(CATEGORIES, ({ value }) => {
    newConfig[value] = [];
  });

  forEach(config, (value, key) => {
    const keyArr = key.split('_');
    const featureValue = parseInt(value, 10) || 0;
    if (featureValue > 0) {
      // enabled
      if (
        keyArr.length === 2 ||
        (keyArr.length === 3 && ['platform', 'misc'].includes(keyArr[0]))
      ) {
        const category = CATEGORIES.find(
          (categoryItem) => keyArr[0].indexOf(categoryItem.key) === 0,
        );
        if (category) {
          let feature = keyArr[1];
          if (keyArr[2]) {
            feature = `${keyArr[1]}_${keyArr[2]}`;
          }
          if (
            ['evpn', 'l3', 'l2'].includes(category.key) &&
            ['bgp', 'udld'].includes(keyArr[1])
          ) {
            // l3_udld, l2_udld, l3_bgp, evpn_bgp
            feature = `${category.key}_${feature}`;
          }
          newConfig[category.value].push(feature);
        }
      }
    }

    if (keyArr[keyArr.length - 1] === 'count' || key === 'mac') {
      newConfig.featureCounts[key] = featureValue;
    }
    if (
      [
        'retailwt',
        'govtwt',
        'healthwt',
        'ngewt',
        'educationwt',
        'financewt',
        'pewt',
        'ngevpnwt',
        'sdawt',
      ].includes(key)
    ) {
      newConfig.cust_wt[key] = value;
    }
  });

  return newConfig;
};

const uniqueConfig = (array, config,externalCustomersConfig) => {
  const newConfig = convertConfig(config);  
  if(externalCustomersConfig && Array.isArray(externalCustomersConfig)){
    const cust_segment = Number(newConfig.cust_segment)
    if(!isNaN(cust_segment)){
      newConfig.cust_segment = cust_segment
    }
    const cloneNewConfig = cloneDeep(newConfig)
    externalCustomersConfig.push(cloneNewConfig)
  }
  const indexConfig = array.findIndex(
    (item) => item.cust_id === config.cust_id,
  );
  if (indexConfig < 0) {
    INTERNAL_CUST_SEGMENT.forEach((item) => {
      if (Number(newConfig.cust_segment) === Number(item.value)) {
        newConfig.cust_segment = Number(item.value)
      }
    })
    array.push(newConfig);
  } else {
    forEach(CATEGORIES, ({ value }) => {
      const oldData = array[indexConfig][value];
      const newData = newConfig[value];
      // eslint-disable-next-line no-param-reassign
      array[indexConfig][value] = [...new Set(newData.concat(oldData))];
    });


    if(newConfig.techsupport_sw_type){
      array[indexConfig].techsupport_sw_type = String(newConfig.techsupport_sw_type)
    }

    // featureCounts
    const oldFeatureCounts = array[indexConfig].featureCounts;
    const newFeatureCounts = newConfig.featureCounts;
    forEach(newFeatureCounts, (value, feature) => {
      if (feature in oldFeatureCounts === false) {
        oldFeatureCounts[feature] = value;
      } else {
        oldFeatureCounts[feature] += value;
      }
    });
  }
};

/**
 * Get all config of internal/ external customer
 * @param {*} config
 * @returns
 */
export const getTotalConfigs = (config) => {
  let total = [];
  forEach(config, (value, key) => {
    if (
      ![
        'featureCounts',
        'cust_id',
        'sameConfigs',
        'cust_segment',
        'cust_wt',
        'techsupport_sw_type'
      ].includes(key)
    ) {
      total = [...total, ...value];
    }
  });
  return total;
};

export const getUniqueData = (
  results,
  externalCustomers,
  internalCustomers = [],
  externalCustomersConfig,
) => {
  forEach(results, (config) => {
    if (Number.isNaN(parseInt(config.cust_id, 10))) {
      // id is text string
      uniqueConfig(internalCustomers, config);
    } else {
      uniqueConfig(externalCustomers, config,externalCustomersConfig);
    }
  });
};

const getMatchData = async (internalCustomers, externalCustomers) => {
  let sameCustomerIds = new Set();
  
  forEach(internalCustomers, (internalConfig, key) => {
    const totalInternalConfig = getTotalConfigs(internalConfig);
    internalCustomers[key].sameConfigs = [];

    forEach(externalCustomers, (externalConfig) => {
      if (internalConfig.cust_segment === externalConfig.cust_segment) {
        const totalExternalConfig = getTotalConfigs(externalConfig);
        const intersectionData = intersection(
          totalInternalConfig,
          totalExternalConfig,
        );

        const samePercent = Number(
          parseFloat(
            (intersectionData.length / totalExternalConfig.length) * 100,
          ).toFixed(2),
        );
        internalCustomers[key].sameConfigs.push({
          cust_id: externalConfig.cust_id,
          value: samePercent,
        });
        sameCustomerIds.add(externalConfig.cust_id);
      }
    });
  });

  // other config
  const categories = (await RedisService.get('categories')) || [];

  sameCustomerIds = [...sameCustomerIds];
  const othersConfig = { cust_id: 'others', sameConfigs: [] };
  forEach(categories, (value, key) => {
    othersConfig[key] = value;
  });
  internalCustomers.push(othersConfig);
  forEach(externalCustomers, (externalConfig) => {
    if (!sameCustomerIds.includes(externalConfig.cust_id)) {
      othersConfig.sameConfigs.push({
        cust_id: externalConfig.cust_id,
        value: getTotalConfigs(externalConfig).length,
      });
    }
  });
};

export const handleGetDataGlobalFeature25 = (results = [])=>{
  const dataGlobalFeature25Convert = {}
  const platformList = []
  results.forEach((item)=>{
    const templateFeatures = `{"${item.features.replaceAll(`,`,`","`).replaceAll(`:`,`":"`)}"}`
    if(!dataGlobalFeature25Convert['features']){
      dataGlobalFeature25Convert['features'] = {}
    }
    
    dataGlobalFeature25Convert['features'][item.platform] = JSON.parse(templateFeatures)

    platformList.push(item.platform)
  })
  dataGlobalFeature25Convert.platformList = platformList;
  return dataGlobalFeature25Convert

}

export const handleConfigData = async (results) => {
  const internalCustomers = []; // chu
  const externalCustomers = []; // so
  const externalCustomersConfig = []; // so khong filter id
  const categories = {};
  const totalRecords = results.length;

  getCategories(results, categories);

  externalCustomersConfig.configGetAll = true
  //merge các data có ID giống nhau
  getUniqueData(results, externalCustomers, internalCustomers,externalCustomersConfig);

  await getMatchData(internalCustomers, externalCustomers,externalCustomersConfig);
  RedisService.set('internalCustomers', internalCustomers);
  RedisService.set('externalCustomers', externalCustomers);
  RedisService.set('totalRecords', totalRecords);
  RedisService.set('categories', categories);
  RedisService.set('externalCustomersConfig', externalCustomersConfig);

};

export const handleConfigScaleData = async (results) => {
  const internalCustomers = []; // chu
  const externalCustomers = []; // so
  const categoriesScale = {};
  // console.log(results);
  // results.forEach(item => {
  //   categoriesScale.scaleFeatureType
  // })
  // // await getMatchData(internalCustomers, externalCustomers);
  // // RedisService.set('internalCustomers', internalCustomers);
  // // RedisService.set('externalCustomers', externalCustomers);
  // // RedisService.set('totalRecords', totalRecords);
  RedisService.set('categoriesScale', results);
};

export const saveOneConfig = async (results) => {
  const externalCustomers = (await RedisService.get('externalCustomers')) || [];
  const externalCustomerData = [];
  getUniqueData(results, externalCustomerData);
  const externalCustomer = externalCustomerData[0];
  externalCustomers.push(externalCustomer);
  RedisService.set('externalCustomers', externalCustomers);

  return externalCustomer;
};

// compare config by external customer id
export const handleConfigDataByCustomer = async (externalCustomer) => {
  let result = [];
  let internalCustomers = (await RedisService.get('internalCustomers')) || [];
  const totalExternalConfig = getTotalConfigs(externalCustomer);

  const custSegment = externalCustomer.cust_segment;

  if (custSegment) {
    const internalCustomer = internalCustomers.find(
      (cust) => cust.cust_segment == custSegment,
    );

    if (internalCustomer) {
      internalCustomers = internalCustomers.filter(
        (i) => i.cust_id !== internalCustomer.cust_id,
      );
    }
    const totalInternalConfig = getTotalConfigs(internalCustomer);
    const intersectionData = intersection(
      totalInternalConfig,
      totalExternalConfig,
    );
    const samePercent = Number(
      parseFloat(
        (intersectionData.length / totalExternalConfig.length) * 100,
      ).toFixed(2),
    );

    result.push({
      cust_id: internalCustomer.cust_id,
      value: samePercent,
      
    });
  }

  const chartData = [];
  forEach(internalCustomers, (internalConfig) => {
    if (internalConfig.cust_id !== 'others') {
      const totalInternalConfig = getTotalConfigs(internalConfig);
      const intersectionData = intersection(
        totalInternalConfig,
        totalExternalConfig,
      );
      const samePercent = Number(
        parseFloat(
          (intersectionData.length / totalExternalConfig.length) * 100,
        ).toFixed(2),
      );
      chartData.push({
        cust_id: internalConfig.cust_id,
        value: samePercent,
      });
    }
  });

  result = [...result, ...chartData.sort((a, b) => b.value - a.value)];
  return result;
};

export const getExternalCustomerSummaryInfo = async (externalCustomer) => {
  const internalCustomers = (await RedisService.get('internalCustomers')) || [];
  const totalConfig = getTotalConfigs(externalCustomer);
  let dataCombine = { data: [], type: COVERED_BY_COMBINATION };

  const dataMatch = await handleConfigDataByCustomer(externalCustomer);
  if (dataMatch[0].value === 100) {
    const dataCoveredByCombination = dataMatch.filter(
      (item) => item.value === 100,
    );
    // .map((item) => item.cust_id);

    if (dataCoveredByCombination.length > 0) {
      dataCombine = {
        type: COVERED,
        data: dataCoveredByCombination,
      };
      return { cust_id: externalCustomer.cust_id, dataCombine, totalConfig };
    }
  }

  let tempConfig = [...totalConfig];
  let tempNumberOfConfig = tempConfig.length;

  dataMatch.forEach((data) => {
    const internalCustomer = internalCustomers.find(
      (item) => item.cust_id === data.cust_id,
    );

    const internalConfig = getTotalConfigs(internalCustomer);
    tempConfig = difference(tempConfig, internalConfig);

    const combinePercent = Number(
      parseFloat(
        ((tempNumberOfConfig - tempConfig.length) / totalConfig.length) * 100,
      ).toFixed(2),
    );

    if (combinePercent) {
      dataCombine.data.push({
        cust_id: internalCustomer.cust_id,
        value: combinePercent,
      });
    }
    tempNumberOfConfig = tempConfig.length;
  });

  if (tempConfig.length) {
    dataCombine = {
      data: tempConfig,
      type: NOT_COVERED,
    };
  }

  return { cust_id: externalCustomer.cust_id, dataCombine, totalConfig };
};

export const getConfigDataCombine = async (totalConfig) => {
  const internalCustomers = (await RedisService.get('internalCustomers')) || [];
  const dataMatch = [];
  forEach(internalCustomers, (internalConfig) => {
    if (internalConfig.cust_id !== 'others') {
      const totalInternalConfig = getTotalConfigs(internalConfig);
      const intersectionData = intersection(totalInternalConfig, totalConfig);
      const samePercent = Number(
        parseFloat(
          (intersectionData.length / totalConfig.length) * 100,
        ).toFixed(2),
      );
      dataMatch.push({
        cust_id: internalConfig.cust_id,
        value: samePercent,
      });
    }
  });

  let dataCombine = { data: [], type: COVERED_BY_COMBINATION };

  const dataCoveredByCombination = dataMatch
    .filter((item) => item.value === 100)
    .map((item) => item.cust_id);

  if (dataCoveredByCombination.length > 0) {
    dataCombine = {
      type: COVERED,
      data: dataCoveredByCombination,
    };
    return { dataCombine, totalConfig };
  }

  let tempConfig = [...totalConfig];
  let tempNumberOfConfig = tempConfig.length;

  dataMatch.forEach((data) => {
    const internalCustomer = internalCustomers.find(
      (item) => item.cust_id === data.cust_id,
    );

    const internalConfig = getTotalConfigs(internalCustomer);
    tempConfig = difference(tempConfig, internalConfig);

    const combinePercent = Number(
      parseFloat(
        ((tempNumberOfConfig - tempConfig.length) / totalConfig.length) * 100,
      ).toFixed(2),
    );

    if (combinePercent) {
      dataCombine.data.push(internalCustomer.cust_id);
    }
    tempNumberOfConfig = tempConfig.length;
  });

  if (tempConfig.length) {
    dataCombine = {
      data: tempConfig,
      type: NOT_COVERED,
    };
  }

  return { dataCombine, totalConfig };
};

export const getScaleDataCombine = async (conditions) => {
  const internalCustomers = (await RedisService.get('internalCustomers')) || [];
  let dataMatch = [];

  forEach(internalCustomers, (customer) => {
    const { featureCounts, cust_id } = customer;
    const dataFeatureCounts = [];
    if (cust_id !== 'others') {
      for (let i = 0; i < conditions.length; i += 1) {
        const condition = conditions[i];
        const { name, value, operator } = condition;
        if (featureCounts[name]) {
          switch (operator) {
            case OPERATOR.GREATER:
              if (featureCounts[name] > value) dataFeatureCounts.push(name);
              break;
            case OPERATOR.GREATER_OR_EQUAL:
              if (featureCounts[name] < value) dataFeatureCounts.push(name);
              break;
            case OPERATOR.LESS:
              if (featureCounts[name] >= value) dataFeatureCounts.push(name);
              break;
            case OPERATOR.LESS_OR_EQUAL:
              if (featureCounts[name] > value) dataFeatureCounts.push(name);
              break;
            case OPERATOR.NOT_EQUAL:
              if (featureCounts[name] === value) dataFeatureCounts.push(name);
              break;
            case OPERATOR.EQUAL:
              if (featureCounts[name] !== value) dataFeatureCounts.push(name);
              break;
            default:
              break;
          }
        }
      }

      dataMatch.push({
        cust_id,
        dataFeatureCounts,
      });
    }
  });
  let dataCombine = { data: [], type: COVERED_BY_COMBINATION };
  dataMatch = dataMatch.sort(
    (a, b) => b.dataFeatureCounts.length - a.dataFeatureCounts.length,
  );
  const dataCoveredByCombination = dataMatch
    .filter((item) => item.dataFeatureCounts.length === conditions.length)
    .map((item) => item.cust_id);

  if (dataCoveredByCombination.length > 0) {
    dataCombine = {
      type: COVERED,
      data: dataCoveredByCombination,
    };
    return { dataCombine, conditions };
  }

  let tempConfig = [...conditions].map((item) => item.name);
  dataMatch.forEach((internalCustomer) => {
    const { dataFeatureCounts, cust_id } = internalCustomer;
    if (tempConfig.length > 0) {
      dataCombine.data.push(cust_id);
    }
    tempConfig = difference(tempConfig, dataFeatureCounts);
  });

  if (tempConfig.length) {
    dataCombine = {
      data: tempConfig,
      type: NOT_COVERED,
    };
  }
  return dataCombine;
};

export const getInternalCustomerSummaryInfo = async (customer) => {
  const { cust_id, sameConfigs } = customer;
  const totalConfig = getTotalConfigs(customer);
  return {
    cust_id,
    totalConfig,
    totalExternalCustomerMatch: sameConfigs.length,
  };
};
