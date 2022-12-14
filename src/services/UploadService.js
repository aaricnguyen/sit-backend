/* eslint-disable quotes */
/* eslint-disable camelcase */
/* eslint-disable import/prefer-default-export */
import createError from 'http-errors';
import status from 'http-status';
import unzipper from 'unzipper';
import fs from 'fs';
import { map, random } from 'lodash';
import multer from 'multer';
import path from 'path';
import * as RedisService from './RedisService';

const FILE_TYPES = [
  'application/octet-stream',
  'application/zip',
  'application/json',
  'application/x-zip-compressed',
];
const configDir = 'src/utils/cfgFiles';
const templateDir = 'src/components/Insight';

const getNameFile = async (file) => {
  const extFile = path.extname(file.originalname);
  const externalCustomers = (await RedisService.get('externalCustomers')) || [];
  const externalCustomerIds = map(externalCustomers, 'cust_id');
  let newCustomerID = random(1, 999999);
  while (externalCustomerIds.includes(newCustomerID)) {
    newCustomerID = random(1, 999999);
  }
  return `${newCustomerID}${extFile}`;
};

export const handleZipFie = async (req, res, next) => {
  const { file } = req;
  const fileNamesList = [];

  const cust_id = parseInt(file.filename, 10);
  req.cust_id = cust_id;
  if (file.mimetype === 'application/octet-stream') {
    req.fileNamesList = [file.filename];
    return next();
  }

  await fs
    .createReadStream(file.path)
    .pipe(unzipper.Parse())
    .on('entry', (entry) => {
      const extFile = path.extname(entry.path);
      if (extFile === '.cfg') {
        const newFileName = `${cust_id}_${fileNamesList.length + 1}${extFile}`;
        fileNamesList.push(newFileName);
        entry.pipe(fs.createWriteStream(`${configDir}/${newFileName}`));
      } else {
        entry.autodrain();
      }
    })
    .promise();

  fs.unlinkSync(file.path);
  if (fileNamesList.length < 1) {
    next(createError(status.BAD_REQUEST, "The zip file's data is invalid."));
  }
  req.fileNamesList = fileNamesList;
  next();
};

export const setUploader = (req, res, next) => {
  const storage = multer.diskStorage({
    destination(_req, file, cb) {
      if (file.mimetype === 'application/octet-stream') {
        cb(null, configDir);
      } else {
        cb(null, `${configDir}/temp`);
      }
    },
    filename: async (_req, file, cb) => {
      cb(null, await getNameFile(file));
    },
  });

  const upload = multer({
    storage,
    fileFilter: (_req, file, cb) => {
      try {
        if (!FILE_TYPES.includes(file.mimetype)) {
          next(
            createError(
              status.BAD_REQUEST,
              'Uploaded file is not a valid configuration file.',
            ),
          );
        }
        cb(null, true);
      } catch (error) {
        cb(error, false);
      }
    },
  });

  const data = upload.single('file');
  data(req, res, (error) => {
    if (error) {
      next(createError(status.BAD_REQUEST, error));
    }
    next();
  });
};

export const setUploaderTemplate = (req, res, next) => {
  const storage = multer.diskStorage({
    destination(_req, file, cb) {
      if (file.mimetype === 'application/json') {
        cb(null, templateDir);
      } else {
        cb(null, `${templateDir}/temp`);
      }
    },
    filename: async (_req, file, cb) => {
      cb(null, 'template.json');
    },
  });

  const upload = multer({
    storage,
    fileFilter: (_req, file, cb) => {
      try {
        if (!FILE_TYPES.includes(file.mimetype)) {
          next(
            createError(
              status.BAD_REQUEST,
              'Uploaded file is not a valid configuration file.',
            ),
          );
        }
        cb(null, true);
      } catch (error) {
        cb(error, false);
      }
    },
  });

  const data = upload.single('file');
  data(req, res, (error) => {
    if (error) {
      next(createError(status.BAD_REQUEST, error));
    }
    next();
  });
};
