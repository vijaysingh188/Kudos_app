// src/services/auth.js
const authService = {
  getCurrentUser: () => Promise.resolve({ 
    username: 'demo', 
    organization: { name: 'Demo Org' },
    remaining_kudos: 3 
  })
};

export const getToken = () => localStorage.getItem('token'); // Added getToken function

export default authService;