import { Navigate } from 'react-router-dom';
import { getToken } from '../../services/auth';

const PrivateRoute = ({ children }) => {
  const isAuthenticated = getToken(); // Check if user has token

  return isAuthenticated ? children : <Navigate to="/login" />;
};

export default PrivateRoute;