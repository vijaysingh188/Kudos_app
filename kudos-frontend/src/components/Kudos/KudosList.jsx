import { Card, CardContent, Typography } from '@mui/material';

const KudosList = ({ kudos }) => {
  return (
    <Card>
      <CardContent>
        <Typography variant="h6" gutterBottom>
          Received Kudos
        </Typography>
        {kudos.map(kudo => (
          <div key={kudo.id} style={{ marginBottom: '1rem' }}>
            <Typography variant="subtitle1">
              From: {kudo.from_user.username}
            </Typography>
            <Typography variant="body2">
              {kudo.message}
            </Typography>
          </div>
        ))}
      </CardContent>
    </Card>
  );
};

export default KudosList;