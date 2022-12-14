/* eslint-disable no-restricted-syntax */
import fs from 'fs';
import { confDefaultTrueList, template, withoutConfList } from './template';

export const parseConfigByFeature = (dataFile, feature) => {
  let dataConfig = dataFile.match(template[feature]) || [];
  if (feature in withoutConfList) {
    dataConfig = dataConfig.filter(
      (config) => !config.includes(withoutConfList[feature]),
    );
  }

  if (confDefaultTrueList.includes(feature) && dataConfig.length === 0) {
    dataConfig = [`${feature} is enabled by default`];
  }
  return dataConfig;
};

export const parseConfigById = (custId, featureList) => {
  const data = {};
  const dir = './src/utils/cfgFiles';
  const files = fs.readdirSync(dir);
  for (const file of files) {
    if (new RegExp(`^${custId}_?.*.cfg$`).test(file)) {
      const dataFile = fs.readFileSync(`${dir}/${file}`, 'utf8');
      featureList.forEach((feature) => {
        const dataConfig = parseConfigByFeature(dataFile, feature);
        if (!data[feature]) data[feature] = [];
        if (dataConfig.length > 0) data[feature].push({ file, dataConfig });
      });
    }
  }
  return data;
};

export const parseUniqConfigById = (custId) => {
  const data = [];
  const dir = './src/utils/cfgFiles';
  const files = fs.readdirSync(dir);
  for (const file of files) {
    if (new RegExp(`^${custId}_?.*.cfg.runn.dup.uniq`).test(file)) {
      const dataFile = fs.readFileSync(`${dir}/${file}`, 'utf8');
      data.push({ file, dataFile });
    }
  }

  return data;
};
