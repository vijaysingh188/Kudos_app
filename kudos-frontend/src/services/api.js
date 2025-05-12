import axios from 'axios';

const api = axios.create({
  baseURL: 'http://localhost:8000/api/', // Added trailing slash to baseURL
});

// Add a request interceptor to include the token in the headers
api.interceptors.request.use((config) => {
  const token = localStorage.getItem('token');
  if (token) {
    config.headers.Authorization = `Token ${token}`;
  }
  return config;
});

export default api;