import { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { Grid, Typography, Box, CircularProgress } from '@mui/material';
import GiveKudos from '../components/Kudos/GiveKudos';
import KudosList from '../components/Kudos/KudosList';
import UserList from '../components/Users/UserList';
import api from '../services/api';

const Dashboard = () => {
  const [user, setUser] = useState(null);
  const [users, setUsers] = useState([]);
  const [kudos, setKudos] = useState([]);
  const [loading, setLoading] = useState(true);
  const navigate = useNavigate();

  useEffect(() => {
    const fetchData = async () => {
      try {
        // Fetch all data in parallel
        const [usersRes, kudosRes] = await Promise.all([
          api.get('/users/'),
          api.get('/kudos/')
        ]);
        
        if (!usersRes.data || usersRes.data.length === 0) {
          console.error('No users found');
        }

        setUsers(usersRes.data);
        setKudos(kudosRes.data);
        
        const meRes = await api.get('/users/me/'); // Fetch actual user data
        setUser(meRes.data); // Set actual user data
        
      } catch (error) {
        console.error('Error fetching data:', error);
        navigate('/login'); // Redirect if needed
      } finally {
        setLoading(false);
      }
    };
    
    fetchData();
  }, [navigate]);

  const handleKudoGiven = (newKudo) => {
    setKudos([newKudo, ...kudos]);
  };

  if (loading) {
    return (
      <Box display="flex" justifyContent="center" mt={5}>
        <CircularProgress />
      </Box>
    );
  }

  return (
    <Box sx={{ p: 3 }}>
      <Typography variant="h4" gutterBottom>
        Welcome, {user?.username}!
      </Typography>
      <Typography variant="subtitle1" gutterBottom>
        Organization: {user?.organization?.name} | 
        Kudos remaining: {user?.remaining_kudos}
      </Typography>
      
      <Grid container spacing={3}>
        <Grid item xs={12} md={4}>
          <GiveKudos 
            users={users.filter(u => u.id !== user?.id)} 
            onKudoGiven={handleKudoGiven} 
            remainingKudos={user?.remaining_kudos || 0}
          />
        </Grid>
        <Grid item xs={12} md={4}>
          <UserList users={users} currentUser={user} />
        </Grid>
        <Grid item xs={12} md={4}>
          <KudosList kudos={kudos} />
        </Grid>
      </Grid>
    </Box>
  );
};

export default Dashboard;