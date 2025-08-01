import React from 'react';
import {
  Typography,
  Grid,
  Paper,
  Box,
} from '@mui/material';

const Dashboard: React.FC = () => {
  return (
    <Box>
      <Typography variant="h4" gutterBottom>
        Dashboard
      </Typography>
      <Grid container spacing={3}>
        <Grid item xs={12} md={6} lg={3}>
          <Paper
            sx={{
              p: 2,
              display: 'flex',
              flexDirection: 'column',
              height: 140,
            }}
          >
            <Typography component="h2" variant="h6" color="primary" gutterBottom>
              Templates
            </Typography>
            <Typography component="p" variant="h4">
              0
            </Typography>
            <Typography color="text.secondary" sx={{ flex: 1 }}>
              Total templates
            </Typography>
          </Paper>
        </Grid>
        <Grid item xs={12} md={6} lg={3}>
          <Paper
            sx={{
              p: 2,
              display: 'flex',
              flexDirection: 'column',
              height: 140,
            }}
          >
            <Typography component="h2" variant="h6" color="primary" gutterBottom>
              Documents
            </Typography>
            <Typography component="p" variant="h4">
              0
            </Typography>
            <Typography color="text.secondary" sx={{ flex: 1 }}>
              Documents uploaded
            </Typography>
          </Paper>
        </Grid>
        <Grid item xs={12} md={6} lg={3}>
          <Paper
            sx={{
              p: 2,
              display: 'flex',
              flexDirection: 'column',
              height: 140,
            }}
          >
            <Typography component="h2" variant="h6" color="primary" gutterBottom>
              Validations
            </Typography>
            <Typography component="p" variant="h4">
              0
            </Typography>
            <Typography color="text.secondary" sx={{ flex: 1 }}>
              Completed validations
            </Typography>
          </Paper>
        </Grid>
        <Grid item xs={12} md={6} lg={3}>
          <Paper
            sx={{
              p: 2,
              display: 'flex',
              flexDirection: 'column',
              height: 140,
            }}
          >
            <Typography component="h2" variant="h6" color="primary" gutterBottom>
              Success Rate
            </Typography>
            <Typography component="p" variant="h4">
              0%
            </Typography>
            <Typography color="text.secondary" sx={{ flex: 1 }}>
              Validation success rate
            </Typography>
          </Paper>
        </Grid>
      </Grid>
    </Box>
  );
};

export default Dashboard;
