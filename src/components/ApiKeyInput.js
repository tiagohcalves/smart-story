
// src/components/ApiKeyInput.js
import React, { useState } from 'react';

const ApiKeyInput = ({ setApiKey }) => {
  const [input, setInput] = useState('');

  const handleChange = (event) => {
    setInput(event.target.value);
  };

  const handleSubmit = (event) => {
    event.preventDefault();
    setApiKey(input);
  };

  return (
    <form onSubmit={handleSubmit}>
      <label>
        Enter Google Sheets API Key:
        <input type="password" value={input} onChange={handleChange} />
      </label>
      <button type="submit">Submit</button>
    </form>
  );
};

export default ApiKeyInput;