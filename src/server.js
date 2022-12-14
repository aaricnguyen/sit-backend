import cookieParser from 'cookie-parser';
import cors from 'cors';
import express from 'express';
import helmet from 'helmet';
import morgan from 'morgan';
import mysql from 'mysql';
import { join } from 'path';
import * as config from './configs';
import {
  DATABASE_HOST,
  DATABASE_NAME,
  DATABASE_PASSWORD,
  DATABASE_USER,
} from './configs';
import apiRoute from './routes';
import { internalServerError, pageNotFound } from './utils/errorHandler';
import logger from './utils/logger';

const app = express();
const server = require('http').createServer(app);

// connect database
global.con = mysql.createConnection({
  host: DATABASE_HOST,
  user: DATABASE_USER,
  password: DATABASE_PASSWORD,
  database: DATABASE_NAME,
});

const corsOptions = {
  origin: config.WEB_URL,
  optionsSuccessStatus: 200, // some legacy browsers (IE11, various SmartTVs) choke on 204
};

app.use(helmet());
app.use(helmet.noSniff()); // set X-Content-Type-Options header
app.use(helmet.frameguard()); // set X-Frame-Options header
app.use(helmet.xssFilter()); // set X-XSS-Protection header
app.use(morgan('dev'));
app.use(express.json());
app.use(express.urlencoded({ extended: false }));
app.use(cookieParser());
app.use(express.static(join(__dirname, 'public')));
app.use(cors(corsOptions));

// route
app.use('/api', apiRoute);

// error handlers
app.use(pageNotFound);
app.use(internalServerError);

server.listen(config.PORT, () => {
  logger.info(`Server running on port: ${config.PORT}`);
});

process.on('unhandledRejection', (error) => {
  logger.error(`unhandledRejection${error.message}`);
});
