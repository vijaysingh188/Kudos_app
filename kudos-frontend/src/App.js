import { ThemeProvider } from '@mui/material/styles';
import CssBaseline from '@mui/material/CssBaseline';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import theme from './styles/theme';
import Login from './pages/Login';
import Dashboard from './pages/Dashboard';
import NotFound from './pages/NotFound';
import Header from './components/Layout/Header';
import PrivateRoute from './components/Auth/PrivateRoute';

function App() {
  return (
    <ThemeProvider theme={theme}>
      <CssBaseline />
      <Router>
        <Header />
        <Routes>
          <Route path="/login" element={<Login />} />
          <Route path="/" element={<PrivateRoute><Dashboard /></PrivateRoute>} />
          <Route path="/users" element={<PrivateRoute><Dashboard /></PrivateRoute>} />
          <Route path="/kudos" element={<PrivateRoute><Dashboard /></PrivateRoute>} />
          {/* <Route path="*" element={<NotFound />} /> */}
        </Routes>
      </Router>
    </ThemeProvider>
  );
}

export default App;