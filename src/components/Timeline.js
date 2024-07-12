// src/components/Home.js
import React, { useState } from 'react';
import GoogleSheetData from './GoogleSheetData';
import { Chrono } from 'react-chrono';
import { Container, Box } from '@mui/material'

const Timeline = ({apiKey, sheetId}) => {
    const [timelineItems, setTimelineItems] = useState([]);

    return (
        <div>
            <GoogleSheetData apiKey={apiKey} sheetId={sheetId} setTimelineItems={setTimelineItems} />
            <Container maxWidth="md">
            <Box
              display="flex"
              flexDirection="column"
              alignItems="center"
              justifyContent="center"
              minHeight="100vh"
            >
              <div style={{ width: "100%", height: "500px" }}>
                <Chrono 
                    items={timelineItems} 
                    allowDynamicUpdate={true}
                    mode="VERTICAL_ALTERNATING" 
                    theme={{
                    primary: 'blue',
                    secondary: 'blue',
                    cardBgColor: 'white',
                    titleColor: 'black',
                    titleColorActive: 'red',
                    }}
                />
              </div>
            </Box>
          </Container>
                
        </div>
    );
};

export default Timeline;