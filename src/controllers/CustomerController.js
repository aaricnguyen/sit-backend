/* eslint-disable no-undef */
/* eslint-disable camelcase */
import { spawn } from 'child_process';
import { difference, forEach, isEmpty } from 'lodash';
import {
  DATABASE_HOST,
  DATABASE_NAME,
  DATABASE_PASSWORD,
  DATABASE_USER,
  NODE_ENV,
} from '../configs';
import { CATEGORIES } from '../constants';
import {
  getExternalCustomerSummaryInfo,
  getTotalConfigs,
  handleConfigData,
  handleConfigDataByCustomer,
  saveOneConfig,
  handleConfigScaleData,
  handleGetDataGlobalFeature25,
  getCategoriesV2,
  getMatchDataV2,
  getSqlQueryUniqueCustomerData,
} from '../services/CustomerService';
import * as RedisService from '../services/RedisService';
import { responseError, responseSuccess } from '../services/Response';
import logger from '../utils/logger';
import { parseConfigById, parseUniqConfigById } from '../utils/parseConfig';

const getColumnCustomerData = (sqlColumnCustomerData)=>{
  return new Promise((resolve, reject) => {
      con.query(sqlColumnCustomerData, async (err, results = []) => {
    if (err) reject(err);
    const listColumns = results.map(item=>item.Field)
    resolve(listColumns)
  });
  });
}

const getUniqueCustomerData = (sqlQueryUniqueCustomerData)=>{
  return new Promise((resolve, reject) => {
      con.query(sqlQueryUniqueCustomerData, async (err, results = []) => {
    if (err) reject(err);
    resolve(results)
  });
  });
}

export const updateV2 = async (req, res) => {
  const selectSacle = 'SELECT * FROM ScaleData';
  con.query(selectSacle, async (err, results) => {
    if (err) throw err;
    await handleConfigScaleData(results);
  });
  const selectTotalRecords = 'SELECT COUNT(*) as totalRecords FROM custConfigDB.customerData'
  con.query(selectTotalRecords, async (err, results) => {
    if (err) throw err;
    RedisService.set('totalRecords', results[0].totalRecords);
  });
  const sqlIgnoreFeatures = 'SELECT * FROM ignore_features';
  con.query(sqlIgnoreFeatures, async (err, results) => {
    if (err) throw err;
    RedisService.set('listIgnoreFeatures',results);
  });

  const sqlColumnCustomerData = 'SHOW COLUMNS FROM custConfigDB.customerData';
  const listColumns = await getColumnCustomerData(sqlColumnCustomerData)
  const {categories,categoriesField,arrQueryUnique} = getCategoriesV2(listColumns)
  RedisService.set('categories',categories);
  
  const sqlQueryUniqueCustomerData = getSqlQueryUniqueCustomerData({
    arrQueryUnique
  })
  
  const uniqueCustomerData = await getUniqueCustomerData(sqlQueryUniqueCustomerData)
  const externalCustomers = []
  const internalCustomers = []
  const internalCustomersObj = {}

  const cust_wt_list = ['retailwt','govtwt','healthwt','ngewt','educationwt','financewt','pewt','ngevpnwt','sdawt']
  const cust_segment_externalCustomers = {}
  const cust_segment_internalCustomers = {}
  const cust_id_internalCustomers = {}

  


  uniqueCustomerData.forEach((config)=>{
    const {cust_id,techsupport_sw_type,cust_segment = -1} = config
    const isInternalCustomers = !!Number.isNaN(parseInt(config.cust_id, 10)) 
    const newItem = {cust_id,techsupport_sw_type,cust_segment,cust_wt:{}}
    if(!cust_segment_externalCustomers[cust_segment]){
      cust_segment_externalCustomers[cust_segment] = []
    }
    if(!cust_segment_internalCustomers[cust_segment]){
      cust_segment_internalCustomers[cust_segment] = []
    }
    if(!cust_id_internalCustomers[cust_id]){
      cust_id_internalCustomers[cust_id] = []
    }
    if(!internalCustomersObj[cust_id]){
      internalCustomersObj[cust_id] = {
        totalConfig : []  
      }
    }
    const totalConfig = []

    Object.keys(categoriesField).forEach(categoryFieldKey=>{
        if(!newItem[categoriesField[categoryFieldKey]]){
          if(categoriesField[categoryFieldKey] !== 'featureCounts'){
          newItem[categoriesField[categoryFieldKey]] = []
          }else{
           newItem[categoriesField[categoryFieldKey]] = {}
          }
        }
        if(categoriesField[categoryFieldKey] !== 'featureCounts'){
          if(!config[categoryFieldKey]){
            return
          }
          totalConfig.push(categoryFieldKey)
          if(isInternalCustomers){
            internalCustomersObj[cust_id].totalConfig.push(categoryFieldKey)
            // newItem.totalConfig.push(categoryFieldKey)
          }
          newItem[categoriesField[categoryFieldKey]].push(categoryFieldKey.replace(/^[^_]*_/,''))
        }else{
          newItem[categoriesField[categoryFieldKey]][categoryFieldKey] = config[categoryFieldKey]
        }
    })
    cust_wt_list.forEach(item=>{
          if(config[item]){
  
            newItem.cust_wt[item] = config[item]
          }
      })
    if (isInternalCustomers) {
      cust_id_internalCustomers[cust_id] = totalConfig
      cust_segment_internalCustomers[cust_segment].push({
        cust_id,
        totalConfig,
      })
      internalCustomers.push(newItem)
    }else{
      cust_segment_externalCustomers[cust_segment].push({
        cust_id,
        totalConfig,
      })
      externalCustomers.push(newItem)
    }    
  })
  getMatchDataV2({
    internalCustomers,
    cust_segment_externalCustomers,
    cust_segment_internalCustomers,
    internalCustomersObj,
    categories
  })
  RedisService.set('internalCustomers', internalCustomers);
  RedisService.set('externalCustomers', externalCustomers);
  RedisService.set('categories', categories);
  RedisService.set('categoriesField', categoriesField);
  return res.json(
    responseSuccess({
      message: 'Successfully updated data.',
    }),
  );

};
export const updateData = (req, res) => {
  const selectSacle = 'SELECT * FROM ScaleData';
  con.query(selectSacle, async (err, results) => {
    if (err) throw err;
    await handleConfigScaleData(results);
  });

  const sql = 'SELECT * FROM customerData';
  con.query(sql, async (err, results) => {
    if (err) throw err;
    await handleConfigData(results);
    return res.json(
      responseSuccess({
        message: 'Successfully updated data.',
      }),
    );
  });
};

export const getGlobalTop25 = (req, res) => {
  const sqlTopGlobal25 = 'SELECT *  FROM global_top25_features';
  const listDataSqL = [getDataSQL(sqlTopGlobal25)]
  Promise.all(listDataSqL)
  .then((results) => {
    const [listTopGlobal25] = results
    const data = handleGetDataGlobalFeature25(listTopGlobal25);
    data.CATEGORIES = CATEGORIES
    return res.json(
      responseSuccess({
        data,
        message: 'Successfully get data.',
      }),
    );
  })
  .catch((err)=>{
    return res.json(
      responseSuccess({
        data:[],
        message: 'Something went wrong',
      }),
    );
  })
}

export const getExternalFeatureConfigBySegment = async (req, res) => {
  const getSumCategory = (_data) => {
    const _sumCat = new Map()
    const _rs = {};
    const count = _data.length

    _data.forEach(_item => {
      const {featureCounts} = _item;
      if(featureCounts){
        Object.keys(featureCounts).forEach((key,index)=>{
          if(!_rs[key]){
            _rs[key] = {min:0,max:0,indexx:0}
          }

          const _value =  _rs[key] &&  _rs[key].sum >= 0 ? _rs[key].sum : 0;
          let min = _rs[key].min < featureCounts[key] ?  _rs[key].min : featureCounts[key]
          let max = _rs[key].max > featureCounts[key] ?  _rs[key].max : featureCounts[key]
          let indexx = _rs[key].max > featureCounts[key] ?  _rs[key].indexx : index;
          const _newValue = (featureCounts[key] || 0) - 0
          
          _rs[key] = {
            feature: key,
            total: count,
            sum: _value + _newValue,
            max,
            min,
            indexx
          }
        })
      }
      const a = _rs
      Object.keys(_rs).forEach(key => {
        const value = _rs[key]['sum'] / count;
        _rs[key]['avg'] =  Math.round( value * 10) / 10
      })

    CATEGORIES.forEach(cat => {
      const {value: _key} = cat;
        const _value = _item[_key];
        if(_value && Array.isArray(_value)){
          if(!_sumCat.get(_key)){
            _sumCat.set(_key,[])
          }
          const currentSumCat = _sumCat.get(_key)
          currentSumCat.push.apply(currentSumCat,_value)

          _sumCat.set(_key,currentSumCat)
        }
      })
    })

  return {_rs,_sumCat:Object.fromEntries(_sumCat)}; 
  }

  const getAvg = (_data) => {
    const _rs = {};
    const count = _data.length
    _data.forEach(i => {
      // console.log("data : ........", i)
      const {featureCounts} = i;
      if(featureCounts){
        Object.keys(featureCounts).forEach(key=>{
          const _value =  _rs[key] &&  _rs[key].sum >= 0 ? _rs[key].sum : 0;
          let min = _rs[key] &&  _rs[key].min >= 0 ? _rs[key].min : 0;
          let max = _rs[key] &&  _rs[key].max >= 0 ? _rs[key].max : 0;
          const _newValue = (featureCounts[key] || 0) - 0
          max = _newValue >  max ? _newValue : max;
          min = _newValue < min ? _newValue : min;
          _rs[key] = {
            feature: key,
            total: count,
            sum: _value + _newValue,
            max,
            min
          }
        })
      }
    })
    Object.keys(_rs).forEach(key => {
      const value = _rs[key]['sum'] / count;
      _rs[key]['avg'] =  Math.round( value * 10) / 10
    })
    return _rs
  }

  //main function process
  const {custom_segment,sw} = req.query
  const externalCustomers = (await RedisService.get('externalCustomersConfig')) || [];
  // console.log("..............externalCustomers: " + externalCustomers)
  let avg = {};
  let count = 0;
  let sum = {};

  if(Array.isArray(externalCustomers) && externalCustomers.length > 0){
    const externalCustomersBySegment = externalCustomers.filter(i => {
      const regex = new RegExp(`[a-zA-Z\s]+${sw}`) ;
      const isFilterSW = sw ? String(i.techsupport_sw_type).match(regex) : true;
      const isFilterSegment = i.cust_segment == custom_segment
      return isFilterSegment && isFilterSW
    } )
    const {_rs,_sumCat}  = getSumCategory(externalCustomersBySegment)
    avg = _rs;
    sum = _sumCat
    count = externalCustomersBySegment.length
  }
  return res.json(responseSuccess({
    message: 'Get successfully.',
    data:  {featureCounts: avg, categories: sum}
  }))
};
const getSumCategoryV2 =  async(_data) => {
  let categoriesField = (await  RedisService.get('categoriesField')) || {};
  if(true){
    const sqlColumnCustomerData = 'SHOW COLUMNS FROM custConfigDB.customerData';
    const listColumns = await getColumnCustomerData(sqlColumnCustomerData)
    const {categoriesField:categoriesF,categories} = getCategoriesV2(listColumns)
    categoriesField = categoriesF
    RedisService.set('categoriesField',categoriesField)
  }
  const _rs = {};
  const count = _data.length
  const _sumCat = new Map()

  _data.forEach(config => {
    Object.keys(config).forEach(field =>{
      if(!config[field]){
        return
      }
      if(categoriesField[field] && categoriesField[field] !== 'featureCounts' ){
        if(!_sumCat.get(categoriesField[field])){
          _sumCat.set(categoriesField[field],[])
        }
        const currentSumCat = _sumCat.get(categoriesField[field])
        currentSumCat.push(field)

        _sumCat.set(categoriesField[field],currentSumCat)

      }
      if(categoriesField[field] && categoriesField[field] === 'featureCounts'){
        if(!_rs[field]){
          _rs[field] = {
            sum: 0,
            max:0,
            min:0,
          }
        } 
        const sum = Number(_rs[field].sum) + Number(config[field])
        const max = _rs[field].max > config[field] ? _rs[field].max : config[field]
        const min = _rs[field].min < config[field] ? _rs[field].min : config[field]
        _rs[field] = {
          feature: field,
          total: count,
          sum,
          max,
          min,
        }
      }
    })

  })
  Object.keys(_rs).forEach(key => {
    const value = _rs[key]['sum'] / count;
    _rs[key]['avg'] =  Math.round( value * 10) / 10
  })

return {_rs,_sumCat:Object.fromEntries(_sumCat)}; 
}
const getDataSQL = (sqlQuery)=>{
  return new Promise((resolve, reject) => {
      con.query(sqlQuery, async (err, results = []) => {
    if (err) reject(err);
    resolve(results)
  });
  });
}
export const getExternalFeatureConfigBySegment2 = async (req, res) => {
  const {custom_segment,sw} = req.query
  const sqlExternalConfig = `SELECT * FROM custConfigDB.customerData WHERE  cust_id REGEXP '^[0-9]+$' ${custom_segment ? `AND cust_segment = ${custom_segment}` : ''} ${sw ? `AND techsupport_sw_type REGEXP '[a-zA-Z\s]+${sw}'` : ''} `
  try {
  const result = await Promise.all([getDataSQL(sqlExternalConfig), RedisService.get('categoriesScale'),RedisService.get('listIgnoreFeatures')])
  const [externalCustomersBySegment,categoriesScale = [],listIgnoreFeatures] = result
  const {_rs,_sumCat}  = await getSumCategoryV2(externalCustomersBySegment)
  return res.json(responseSuccess({
    message: 'Get successfully.',
    data:  {featureCounts:_rs,categories:_sumCat,count:externalCustomersBySegment.length,CATEGORIES,categoriesScale,listIgnoreFeatures}
  })) 
} catch (error) {
  return res.json(responseSuccess({
    message: 'Something went wrong',
    data:  {}
  }))
}
};
export const getExternalFeatureCountBySegment = async (req, res) => {
  const getSumCategory = (_data) => {
    const _sumCat = {};
    _data.forEach(_item => {
      Object.keys(_item).forEach(_key => {
        const _value = _item[_key];
        if(_value && Array.isArray(_value)){
          if(!_sumCat[_key]){
            _sumCat[_key] = [];
          }
          _sumCat[_key] = [..._sumCat[_key], ..._value];
        }
      })
    })
  return _sumCat
  }

  const getAvg = (_data) => {
    const _rs = {};
    const count = _data.length
    _data.forEach(i => {
      // console.log("data : ........", i)
      const {featureCounts} = i;
      if(featureCounts){
        Object.keys(featureCounts).forEach(key=>{
          const _value =  _rs[key] &&  _rs[key].sum >= 0 ? _rs[key].sum : 0;
          let min = _rs[key] &&  _rs[key].min >= 0 ? _rs[key].min : 0;
          let max = _rs[key] &&  _rs[key].max >= 0 ? _rs[key].max : 0;
          const _newValue = (featureCounts[key] || 0) - 0
          max = _newValue >  max ? _newValue : max;
          min = _newValue < min ? _newValue : min;
          _rs[key] = {
            feature: key,
            total: count,
            sum: _value + _newValue,
            max,
            min
          }
        })
      }
    })
    Object.keys(_rs).forEach(key => {
      const value = _rs[key]['sum'] / count;
      _rs[key]['avg'] =  Math.round( value * 10) / 10
    })
    return _rs
  }

  //main function process
  const {custom_segment,sw} = req.query
  const externalCustomers = (await RedisService.get('externalCustomers')) || [];
  // console.log("..............externalCustomers: " + externalCustomers)
  let avg = {};
  let count = 0;
  let sum = {};
  if(Array.isArray(externalCustomers) && externalCustomers.length > 0){
    const externalCustomersBySegment = externalCustomers.filter(i => {
      const regex = new RegExp(`[a-zA-Z\s]+${sw}`) ;
      const isFilterSW = sw ? String(i.techsupport_sw_type).match(regex) : true;
      const isFilterSegment = i.cust_segment == custom_segment
      return isFilterSegment && isFilterSW
    } )
    avg =  getAvg(externalCustomersBySegment)
    sum = getSumCategory(externalCustomersBySegment)
    count = externalCustomersBySegment.length
  }
  return res.json(responseSuccess({
    message: 'Get successfully.',
    data:  {featureCounts: avg, categories: sum,count}
  }))
};

export const getOverview = async (req, res) => {
  const totalRecords = (await RedisService.get('totalRecords')) || 0;
  const externalCustomers = (await RedisService.get('externalCustomers')) || [];
  const internalCustomers = (await RedisService.get('internalCustomers')) || [];
  const categories = (await RedisService.get('categories')) || [];
  const totalConfigs = getTotalConfigs(categories).length || 0;

  return res.json(
    responseSuccess({
      message: 'get overview information successfully.',
      data: {
        totalRecords,
        internalRecords: internalCustomers.filter(
          (item) => item.cust_id !== 'others',
        ).length,
        externalRecords: externalCustomers.length,
        totalConfigs,
      },
    }),
  );
};

export const getChartData = async (req, res) => {
  const {
    typeChart = 1,
    typeChartScale = 1,
    id = null,
    idScale = null,
    category = null,
    internalId = null,
    externalId = null,
    typeDisplay = 'top10',
    _page = 1,
    _perPage = 20,
  } = req.query;

  let dataScaleChart = null;

  const externalCustomers = (await RedisService.get('externalCustomers')) || [];
  const internalCustomers = (await RedisService.get('internalCustomers')) || [];
  const categoriesScale = (await RedisService.get('categoriesScale')) || [];

  let internalConfig = null;
  let externalConfig = null;
  const data = {};
  data.chartData = [];
  data.ScaleData = [];
  let InternalCust = null;
  let ExternalCust = null;
  if (typeChart === '5') {
    ExternalCust = externalId;
    InternalCust = internalId;
  } else {
    ExternalCust = id;
    InternalCust = internalId;
  }
  console.log('type Chart', typeChart);
  console.log('id', InternalCust);
  console.log('external', ExternalCust);
  if (ExternalCust && InternalCust) {
    data.ScaleData = await getScaleChartData(
      ExternalCust,
      InternalCust,
      typeChartScale,
      idScale,
    );
  }
  let perPage = _perPage;
  let page = parseInt(_page, 10);

  if (typeChart > 1 && typeChart <= 5) {
    if (!id) return res.json(responseError({ message: 'Id is required!' }));

    if (typeChart >= 3 && typeChart <= 4) {
      externalConfig = externalCustomers.find((item) => item.cust_id === id);
      if (!externalConfig) {
        return res.json(
          responseError({ message: 'This external customer does not exist!' }),
        );
      }
    }
  }

  if (typeChart >= 3 && typeChart <= 5) {
    if (!internalId) {
      return res.json(responseError({ message: 'internalId is required!' }));
    }
    internalConfig = internalCustomers.find(
      (item) => item.cust_id === internalId,
    );
    if (!internalConfig) {
      return res.json(
        responseError({
          message: 'This internal customer does not exist!',
        }),
      );
    }
  }

  switch (typeChart) {
    // ====================== chart 2 (External Customers) ======================
    case '2':
      internalConfig = internalCustomers.find((item) => item.cust_id === id);
      if (!internalConfig) {
        return res.json(
          responseError({
            message: 'This internalConfig customer does not exist!',
          }),
        );
      }
      data.chartData = [...internalConfig.sameConfigs];
      data.chartData = data.chartData.sort((a, b) => b.value - a.value);
      if (typeDisplay !== 'all') {
        perPage = 10;
        page = 1;
      } else {
        if (page <= 1 || Number.isNaN(page)) page = 1;
        data.pagination = {
          _total: data.chartData.length,
          _page: page,
        };
      }
      data.chartData = data.chartData.slice(
        (page - 1) * perPage,
        page * perPage,
      );
      break;

    // ====================== chart 3 (Category Comparison) ======================
    case '3':
      forEach(externalConfig, (value, key) => {
        const noMatch = difference(value, internalConfig[key]);
        if (
          ![
            'featureCounts',
            'cust_id',
            'sameConfigs',
            'cust_segment',
            'cust_wt',
            'techsupport_sw_type',
          ].includes(key)
        ) {
          data.chartData.push({
            category: key,
            value: value.length,
            internalValue: internalConfig[key].length,
            noMatchValue: noMatch.length,
          });
        }
      });

      break;

    // ====================== chart 4 ======================
    case '4':
      if (!category) {
        return res.json(responseError({ message: 'Category is required!' }));
      }
      if (!CATEGORIES.find((item) => item.value === category)) {
        return res.json(responseError({ message: 'Category is not exists!' }));
      }

      data.chartData = {
        category,
        internalId,
        internalConfig: internalConfig[category],
        externalId: externalConfig.cust_id,
        externalConfig: externalConfig[category],
      };

      break;

    // ====================== chart 5 (show detail config) ======================
    case '5':
      if (!category) {
        return res.json(responseError({ message: 'Category is required!' }));
      }
      if (!CATEGORIES.find((item) => item.value === category)) {
        return res.json(responseError({ message: 'Category is not exists!' }));
      }

      externalConfig = externalCustomers.find(
        (item) => item.cust_id === externalId,
      );
      if (!externalConfig) {
        return res.json(
          responseError({ message: 'This external customer does not exist!' }),
        );
      }

      data.chartData = {
        category,
        feature: id,
        dataConfig: parseConfigById(externalConfig.cust_id, [id])[id],
      };

      break;

    // ====================== chart1 ======================
    default:
      data.chartData = internalCustomers.map((item) => ({
        cust_id: item.cust_id,
        value: item.sameConfigs.length,
        valueOf100: item.sameConfigs.filter((conf) => conf.value === 100)
          .length,
        valueOf90: item.sameConfigs.filter(
          (conf) => conf.value < 100 && conf.value >= 90,
        ).length,
        valueOf80: item.sameConfigs.filter(
          (conf) => conf.value < 90 && conf.value >= 80,
        ).length,
        valueOfBelow80: item.sameConfigs.filter((conf) => conf.value < 80)
          .length,
      }));
      break;
  }
  return res.json(
    responseSuccess({
      message: 'get data of chart successfully.',
      data,
    }),
  );
};

export const getScaleChartData = async (
  externalId,
  internalId,
  typeChartScale,
  idScale,
) => {
  const externalCustomers = (await RedisService.get('externalCustomers')) || [];
  const internalCustomers = (await RedisService.get('internalCustomers')) || [];
  const categoriesScale = (await RedisService.get('categoriesScale')) || [];
  const ScaleData = [];

  const externalConfig = externalCustomers.find(
    (item) => item.cust_id === externalId,
  );
  const internalConfig = internalCustomers.find(
    (item) => item.cust_id === internalId,
  );

  if (parseInt(typeChartScale) === 1) {
    categoriesScale.forEach((FeatureType) => {
      // let totalInternal = 0;
      // let totalExternal = 0;
      let count_ex = 0,
        count_in = 0;
      FeatureType.scaleFeatures.split(',').forEach((key) => {
        if (!key) return;
        let num_ex = 0,
          num_in = 0;
        // externalConfig.forEach((external) => {
        //   num_ex = external.featureCounts[key] || 0;
        //   console.log('featureCounts external :', ext.featureCounts[key], key);
        //   internalConfig.forEach((internal) => {
        //     console.log(
        //       'featureCounts internal :',
        //       inter.featureCounts[key],
        //       key,
        //     );
        //     num_in = internal.featureCounts[key] || 0;
        //     if (num_ex > num_in) count_ex++;
        //     else if (num_ex < num_in) count_in++;
        //     else {
        //       count_in++;
        //       count_ex++;
        //     }
        //   });
        // });

        num_ex = externalConfig.featureCounts[key];
        num_in = internalConfig.featureCounts[key];
        if (num_ex > num_in) count_ex++;
        else if (num_ex < num_in) count_in++;
        else {
          if (num_ex > 0 && num_in > 0) {
            count_in++;
            count_ex++;
          }
        }
      });

      ScaleData.push({
        category: FeatureType.scaleFeatureType,
        value: count_ex,
        internalValue: count_in,
      });
    });
  }
  if (parseInt(typeChartScale) === 2) {
    const FeatureScale = categoriesScale.filter(
      (type) => type.scaleFeatureType === idScale,
    );
    if (!FeatureScale) return;

    FeatureScale[0].scaleFeatures.split(',').forEach((key) => {
      if (!key) return;
      ScaleData.push({
        category: key,
        value: externalConfig.featureCounts[key],
        internalValue: internalConfig.featureCounts[key],
      });
    });
  }
  return ScaleData;
};

export const uploadConfigFile = (req, res) => {
  const { fileNamesList, cust_id } = req;

  const { custSegment } = req.body;

  logger.info('fileNamesList', fileNamesList, fileNamesList.join());
  const exec_command = NODE_ENV === 'production' ? 'python3' : 'python';
  const python = spawn(exec_command, [
    './src/utils/pythonscript/ciscoConfigParser_for_ui.py',
    DATABASE_USER,
    DATABASE_PASSWORD,
    DATABASE_HOST,
    DATABASE_NAME,
    fileNamesList.join(),
  ]);
  python.stdout.on('data', (data) => {
    const bufferOriginal = Buffer.from(data);
    logger.info(bufferOriginal.toString('utf8'));
    if (custSegment > 0) {
      con.query(
        `UPDATE customerData SET cust_segment = ${custSegment} WHERE cust_id = ${cust_id}`,
        async (err, _) => {
          if (err) throw err;
        },
      );
    }

    const sql = `SELECT * FROM customerData WHERE cust_id = ${cust_id}`;
    con.query(sql, async (err, results) => {
      if (err) throw err;
      const externalCustomer = await saveOneConfig(results);
      const dataExternalCombine = await getExternalCustomerSummaryInfo(
        externalCustomer,
      );
      const { dataCombine, totalConfig } = dataExternalCombine;
      const dataUniq = parseUniqConfigById(externalCustomer.cust_id);
      return res.json(
        responseSuccess({
          data: {
            fileNamesList,
            externalCustomer,
            dataCombine,
            totalConfig,
            dataUniq,
          },
          message: 'Successfully updated data.',
        }),
      );
    });
  });
  python.on('close', (code) => {
    console.log(`child process close all stdio with code ${code}`);
  });
};

export const getExternalCustomerCompareById = async (req, res) => {
  const { id } = req.query;

  if (!id) {
    return res.json(
      responseError({
        message: 'id of external customer is required!',
      }),
    );
  }

  const externalCustomers = (await RedisService.get('externalCustomers')) || [];
  const externalCustomer = externalCustomers.find((item) => {
    if (item !== null && item.cust_id === id) {
      return item;
    }
  });
  if (!externalCustomer) {
    return res.json(
      responseError({
        message: `External customer ${id} is not exists!`,
      }),
    );
  }
  const chartData = await handleConfigDataByCustomer(externalCustomer);
  const newChartData = [];
  forEach(externalCustomer.cust_wt, (value, key) => {
    if (key === 'retailwt') {
      newChartData.push({ cust_id: 'retail', value });
    }
    if (key === 'govtwt') {
      newChartData.push({ cust_id: 'government', value });
    }
    if (key === 'healthwt') {
      newChartData.push({ cust_id: 'healthcare', value });
    }
    if (key === 'ngewt') {
      newChartData.push({ cust_id: 'NGE', value });
    }
    if (key === 'ngevpnwt') {
      newChartData.push({ cust_id: 'NGEVPN', value });
    }
    if (key === 'educationwt') {
      newChartData.push({ cust_id: 'education', value });
    }
    if (key === 'financewt') {
      newChartData.push({ cust_id: 'finance', value });
    }
    if (key === 'pewt') {
      newChartData.push({ cust_id: 'PE', value });
    }
    if (key === 'sdawt') {
      newChartData.push({ cust_id: 'SDA', value });
    }
  });
  return res.json(
    responseSuccess({
      message: 'get data of chart successfully.',
      // data: { chartData: [chartData[0]] },
      data: { chartData: newChartData, matchPercent: chartData[0] },
    }),
  );
};

export const getExternalSummaryInfo = async (req, res) => {
  const { id } = req.query;
  const externalCustomers = (await RedisService.get('externalCustomers')) || [];
  const externalCustomer = externalCustomers.find(
    (item) => item.cust_id === id,
  );
  if (!externalCustomer) {
    return res.json(
      responseError({
        message: `External customer ${id} is not exists!`,
      }),
    );
  }
  res.json({
    data: await getExternalCustomerSummaryInfo(externalCustomer),
  });
};

export const search = async (req, res) => {
  const { q } = req.query;
  let externalCustomers = (await RedisService.get('externalCustomers')) || [];
  externalCustomers = externalCustomers.filter(
    (item) => item.cust_id.indexOf(q) > -1,
  );
  const data = [];

  // eslint-disable-next-line no-plusplus
  for (let i = 0; i < externalCustomers.length; i++) {
    // eslint-disable-next-line no-await-in-loop
    const dataCombine = await getExternalCustomerSummaryInfo(
      externalCustomers[i],
    );
    data.push(dataCombine);
  }
  res.json(
    responseSuccess({
      data,
    }),
  );
};

export const getListInternalCustomer = async (req, res) => {
  const internalCustomers = (await RedisService.get('internalCustomers')) || [];

  const data = internalCustomers
    .filter((item) => item.cust_id !== 'others')
    .map(({ cust_id, cust_segment }) => ({
      cust_id,
      cust_segment,
    }))
    .sort((a, b) => a.cust_segment - b.cust_segment);

  res.json(
    responseSuccess({
      data,
    }),
  );
};
