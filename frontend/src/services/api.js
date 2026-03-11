import axios from 'axios';

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:5000/api';

const API = axios.create({
  baseURL: API_BASE_URL,
  withCredentials: true,
  headers: {
    'Content-Type': 'application/json',
  }
});

// Interceptores para debug
API.interceptors.request.use(request => {
  console.log('📤 Enviando:', request.method, request.url, request.data);
  return request;
});

API.interceptors.response.use(
  response => {
    console.log('📥 Recibido:', response.status, response.data);
    return response;
  },
  error => {
    console.error('❌ Error:', error.response?.status, error.response?.data || error.message);
    return Promise.reject(error);
  }
);

// Autenticación
export const login = (username, password) => 
  API.post('/login', { username, password });

export const logout = () => 
  API.post('/logout');

export const getSession = () => 
  API.get('/session');

// Productos
export const getProductos = () => 
  API.get('/productos');

// Ventas
export const registrarVenta = (productos, metodo_pago) => 
  API.post('/ventas', { productos, metodo_pago });

// Admin
export const getEstadisticas = () => 
  API.get('/estadisticas');

// Test
export const testAPI = () =>
  API.get('/test');

export default API;
