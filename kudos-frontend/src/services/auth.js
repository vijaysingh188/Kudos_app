// src/services/auth.js
import api from './api';

const authService = {
  getCurrentUser: async () => {
    try {
      const response = await api.get('/users/me/'); // Fetch actual user data
      return response.data;
    } catch (error) {
      console.error('Error fetching current user:', error);
      return null; // Return null if the user is not authenticated
    }
  }
};

export const getToken = () => localStorage.getItem('token');

export default authService;