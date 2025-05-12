import { List, ListItem, ListItemText, Typography } from '@mui/material';

const UserList = ({ users, currentUser }) => {
  return (
    <div>
      <Typography variant="h6" gutterBottom>
        Team Members
      </Typography>
      <List>
        {users
          .filter(user => currentUser && user.id !== currentUser.id)
          .map(user => (
            <ListItem key={user.id}>
              <ListItemText 
                primary={user.username}
                secondary={user.organization?.name || 'No organization'}
              />
            </ListItem>
          ))}
      </List>
    </div>
  );
};

export default UserList;