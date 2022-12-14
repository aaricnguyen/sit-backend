import dotEnv from 'dotenv';
import { join } from 'path';

const Environment = process.env.NODE_ENV;

if (Environment !== 'production') {
  dotEnv.config({ path: join(__dirname, '../../.example.env') });
} else {
  dotEnv.config();
}

const { env } = process;

export const NODE_ENV = env.NODE_ENV || 'development';

export const PORT = parseInt(process.env.PORT || '4500', 10);

export const WEB_URL = env.WEB_URL || 'http://localhost:3000';

// redis
export const REDIS_URL = env.REDIS_URL || 'redis://10.78.96.161';

// database
export const DATABASE_HOST = env.DATABASE_HOST || '10.78.96.161';
export const DATABASE_USER = env.DATABASE_USER || 'a1';
export const DATABASE_NAME = env.DATABASE_NAME || 'custConfigDB';
export const DATABASE_PASSWORD = env.DATABASE_PASSWORD || 'Maglev123!';
