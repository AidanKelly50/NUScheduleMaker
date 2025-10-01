import axios from 'axios';
import { createAxiosDateTransformer } from 'axios-date-transformer';

export const API_URL = 'http://localhost:3001';

export default createAxiosDateTransformer({
  baseURL: API_URL,
  withCredentials: true,
  timeout: 10000,
  paramsSerializer: {
    indexes: null
  }
});

// api for external calls
export const externalApi = axios.create({
  timeout: 10000
});

// support for _retry flag
declare module 'axios' {
  interface AxiosRequestConfig {
    _retry?: boolean;
  }
}
