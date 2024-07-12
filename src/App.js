// src/App.js
import React, { useState } from 'react';
import { BrowserRouter, Route, Routes } from 'react-router-dom';
import Home from './components/Home';
import Timeline from './components/Timeline';


const App = () => {
  const [apiKey, setApiKey] = useState('');
  const [sheetId, setSheetId] = useState('');

  return (
    <BrowserRouter>
      <Routes>
        <Route path="/">
          <Route index element={<Home setApiKey={setApiKey} setSheetId={setSheetId} />} />
          <Route path="/timeline" element={<Timeline apiKey={apiKey} sheetId={sheetId}/>} />
        </Route>
      </Routes>
    </BrowserRouter>
  );
};

export default App;
