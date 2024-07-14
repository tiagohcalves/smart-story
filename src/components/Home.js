// src/components/Home.js
import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { Container, TextField, Button, Typography, Box } from '@mui/material';


const Home = ({ setApiKey, setSheetId }) => {
  const [sheet_id, setLocalSheetId] = useState('');
  const [api_key, setLocalApiKey] = useState('');
  const navigate = useNavigate();

  useEffect(() => {
    const storedApiKey = localStorage.getItem('apiKey');
    if (storedApiKey) {
      setLocalApiKey(storedApiKey);
    }

    const storedSheetId = localStorage.getItem('sheetId');
    if (storedSheetId) {
      setLocalSheetId(storedSheetId);
    }
  }, []);

  const handleChangeSheetId = (event) => {
    setLocalSheetId(event.target.value);
  };

  const handleChangeApiKey = (event) => {
    setLocalApiKey(event.target.value);
  };

  const handleSubmit = (event) => {
    event.preventDefault();
    localStorage.setItem('sheetId', sheet_id);
    localStorage.setItem('apiKey', api_key);
    setSheetId(sheet_id);
    setApiKey(api_key);
    navigate('timeline');
  };

  return (
    <Container maxWidth="sm">
      <Box
        display="flex"
        flexDirection="column"
        alignItems="center"
        justifyContent="center"
        minHeight="100vh"
      >
        <Typography variant="h4" gutterBottom>
          Smart Story
        </Typography>
        <form onSubmit={handleSubmit}>
        <TextField
            label="Spreadsheet ID"
            variant="outlined"
            fullWidth
            value={sheet_id}
            onChange={handleChangeSheetId}
            margin="normal"
            type="text"
          />
          <TextField
            label="API Key"
            variant="outlined"
            fullWidth
            value={api_key}
            onChange={handleChangeApiKey}
            margin="normal"
            type="password"
          />
          <Button type="submit" variant="contained" color="primary" fullWidth>
            Submit
          </Button>
        </form>
      </Box>
    </Container>
  );
};

export default Home;
