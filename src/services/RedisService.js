/* eslint-disable arrow-body-style */
import redis from 'redis';
import { REDIS_URL } from '../configs';

const redisClient = redis.createClient(REDIS_URL);

export const set = (key, value) => {
  redisClient.set(key, JSON.stringify(value));
};
export const get = (key) => {
  return new Promise((resolve, reject) => {
    redisClient.get(key, (error, data) => {
      if (error) reject(error);
      if (data !== null) resolve(JSON.parse(data));
      resolve();
    });
  });
};
