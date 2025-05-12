import { Card, CardContent, Typography } from '@mui/material';

const KudosCard = ({ kudo }) => {
  return (
    <Card style={{ marginBottom: '1rem' }}>
      <CardContent>
        <Typography variant="subtitle1">
          From: {kudo.from_user.username}
        </Typography>
        <Typography variant="body2">
          {kudo.message}
        </Typography>
      </CardContent>
    </Card>
  );
};

export default KudosCard;