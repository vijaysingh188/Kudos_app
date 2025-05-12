import { useState, useEffect } from 'react';
import { Card, CardContent, Typography, TextField, Button, MenuItem, Box } from '@mui/material';
import api from '../../services/api';

const GiveKudos = ({ users, onKudoGiven, remainingKudos }) => {
  const [selectedUser, setSelectedUser] = useState('');
  const [message, setMessage] = useState('');
  const [error, setError] = useState('');

  useEffect(() => {
    console.log('Users prop:', users); // Debugging log to check users prop
  }, [users]);

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!selectedUser || !message) {
      setError('Please select a user and write a message');
      return;
    }

    try {
      console.log('Sending request with token:', localStorage.getItem('token')); // Debugging log for token
      const response = await api.post('/kudos/give_kudo/', {
        to_user_id: selectedUser,
        message
      });
      onKudoGiven(response.data);
      setSelectedUser('');
      setMessage('');
      setError('');
    } catch (err) {
      setError(err.response?.data?.error || 'Failed to send kudo');
    }
  };

  return (
    <Card>
      <CardContent>
        <Typography variant="h6" gutterBottom>
          Give Kudos
        </Typography>
        
        {error && (
          <Typography color="error" sx={{ mb: 2 }}>
            {error}
          </Typography>
        )}

        <Box component="form" onSubmit={handleSubmit}>
          <TextField
            select
            fullWidth
            label="Select a colleague"
            value={selectedUser}
            onChange={(e) => setSelectedUser(e.target.value)}
            margin="normal"
          >
            {users.map((user) => (
              <MenuItem key={user.id} value={user.id}>
                {user.username}
              </MenuItem>
            ))}
          </TextField>
          
          <TextField
            fullWidth
            multiline
            rows={4}
            label="Why are you giving this kudo?"
            value={message}
            onChange={(e) => setMessage(e.target.value)}
            margin="normal"
          />
          
          <Button
            type="submit"
            variant="contained"
            fullWidth
            sx={{ mt: 2 }}
            disabled={remainingKudos <= 0}
          >
            Send Kudo
          </Button>
        </Box>
      </CardContent>
    </Card>
  );
};

export default GiveKudos;