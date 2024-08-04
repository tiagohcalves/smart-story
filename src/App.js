// src/App.js
import React, { useState, useEffect } from 'react';
import { Route, Routes, Link, HashRouter } from 'react-router-dom';
import { AppBar, Toolbar, Typography, Button } from '@mui/material';
import Home from './components/Home';
import Timeline from './components/Timeline';
import ContactList from './components/ContactList';


const App = () => {
  const [apiKey, setApiKey] = useState('');
  const [sheetId, setSheetId] = useState('');

  useEffect(() => {
    const storedApiKey = localStorage.getItem('apiKey');
    if (storedApiKey) {
      setApiKey(storedApiKey);
    }

    const storedSheetId = localStorage.getItem('sheetId');
    if (storedSheetId) {
      setSheetId(storedSheetId);
    }
  }, []);

  return (
    <HashRouter>
      <AppBar position="static">
        <Toolbar>
          <Typography variant="h6" style={{ flexGrow: 1 }}>
            Smart Story
          </Typography>
          <Button color="inherit" component={Link} to="timeline">Timeline</Button>
          <Button color="inherit" component={Link} to="contacts">Contatos</Button>
        </Toolbar>
      </AppBar>
      <Routes>
        <Route path="/">
          <Route index element={<Home setApiKey={setApiKey} setSheetId={setSheetId} />} />
          <Route path="timeline" element={<Timeline apiKey={apiKey} sheetId={sheetId}/>} />
          <Route path="contacts" element={<ContactList apiKey={apiKey} sheetId={sheetId}/>} />
        </Route>
      </Routes>
    </HashRouter>
  );
};

export default App;
