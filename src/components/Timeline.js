// src/components/Home.js
import React, { useState } from 'react';
import GoogleSheetData from './GoogleSheetData';
import { Container, Box, Typography } from '@mui/material'
import { Timeline as PrimeTimeline } from 'primereact/timeline';
import { Card } from 'primereact/card';
import "primereact/resources/themes/lara-light-cyan/theme.css";
import "primereact/resources/primereact.min.css";                  
import "primeicons/primeicons.css";                                


const Timeline = ({apiKey, sheetId}) => {
    const [timelineItems, setTimelineItems] = useState([]);

    const customizedMarker = (item) => {
        return (
            // <span className="flex w-2rem h-2rem align-items-center justify-content-center text-white border-circle z-1 shadow-1" style={{ backgroundColor: item.color }}>
            //     <i className={item.icon}></i>
            // </span>
            <div>
                {item.type}<br/>
                <small>{item.date}</small>
            </div>
        );
    };

    const customizedContent = (item) => {
        return (
            // <Card subTitle={item.date}>
            <Box
                alignItems="center"
                gap={4}
                p={1}
            >{item.prof}
                <p><small>{item.comment}</small> {item.file && <a href={item.file}  target="_blank" rel="noreferrer"> <i className="pi pi-download"></i> </a> }</p></Box>
                
            // </Card>
        );
  };

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
                {/* <Typography variant="h4" gutterBottom>
                    Timeline
                </Typography> */}
                <div className="card">
                    <PrimeTimeline value={timelineItems} opposite={customizedMarker} content={customizedContent} />
                </div>
            </Box>
          </Container>
                
        </div>
    );
};

export default Timeline;