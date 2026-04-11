import axios from 'axios';

const rawBaseUrl = process.env.REACT_APP_API_URL || 'http://localhost:5000/api';
const API_BASE_URL = rawBaseUrl.replace(/\/+$/, '');
const API_TIMEOUT_MS = Number(process.env.REACT_APP_API_TIMEOUT_MS || 15000);
const ENABLE_API_LOGS = process.env.NODE_ENV === 'development' || process.env.REACT_APP_ENABLE_API_LOGS === 'true';

const API = axios.create({
  baseURL: API_BASE_URL,
  withCredentials: true,
  timeout: API_TIMEOUT_MS,
  headers: {
    'Content-Type': 'application/json',
  }
});

if (ENABLE_API_LOGS) {
  API.interceptors.request.use(request => {
    console.log('API request:', request.method, request.url, request.data);
    return request;
  });

  API.interceptors.response.use(
    response => {
      console.log('API response:', response.status, response.data);
      return response;
    },
    error => {
      console.error('API error:', error.response?.status, error.response?.data || error.message);
      return Promise.reject(error);
    }
  );
}

export const login = (username, password) => API.post('/login', { username, password });
export const logout = () => API.post('/logout');
export const getSession = () => API.get('/session');
export const getProductos = () => API.get('/productos');
export const registrarVenta = (productos, metodo_pago) => API.post('/ventas', { productos, metodo_pago });
export const getEstadisticas = () => API.get('/estadisticas');
export const testAPI = () => API.get('/test');

export default API;
