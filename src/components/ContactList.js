// src/components/ContactList.js
import React, { useState, useEffect } from 'react';
import { Container, Typography, List, ListItem, ListItemText, Box } from '@mui/material';
import axios from 'axios';
import { SPREADSHEET_ID, RANGE_CONTACTS } from '../config';

const ContactList = ({ apiKey, sheetId }) => {
  const [contacts, setContacts] = useState([]);

  useEffect(() => {
    const fetchContacts = async () => {
      if (apiKey) {
        const result = await axios.get(
          `https://sheets.googleapis.com/v4/spreadsheets/${sheetId}/values/${RANGE_CONTACTS}?key=${apiKey}`
        );
        const data = result.data.values.map(row => ({
          name: row[0],
          expertise: row[1],
          phone: row[2],
        }));
        setContacts(data);
      }
    };
    fetchContacts();
  }, [apiKey]);

  return (
    <Container maxWidth="md">
      <Box
        display="flex"
        flexDirection="column"
        alignItems="center"
        justifyContent="center"
        minHeight="100vh"
      >
        <Typography variant="h4" gutterBottom>
          Doctors Contact List
        </Typography>
        <List>
          {contacts.map((contact, index) => (
            <ListItem key={index}>
              <ListItemText
                primary={contact.name}
                secondary={`${contact.expertise} - ${contact.phone}`}
              />
            </ListItem>
          ))}
        </List>
      </Box>
    </Container>
  );
};

export default ContactList;
