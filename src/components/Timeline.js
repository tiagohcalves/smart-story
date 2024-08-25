// src/components/Home.js
import React, { useState } from 'react';
import GoogleSheetData from './GoogleSheetData';
import { CircularProgress, Container, Box, Fab, TextField } from '@mui/material'
import AddIcon from '@mui/icons-material/Add';
import { Timeline as PrimeTimeline } from 'primereact/timeline';
import "primereact/resources/themes/lara-light-cyan/theme.css";
import "primereact/resources/primereact.min.css";                  
import "primeicons/primeicons.css";                                

const style = {
    margin: 0,
    top: 'auto',
    right: 20,
    bottom: 20,
    left: 'auto',
    position: 'fixed',
};

const Timeline = ({apiKey, sheetId}) => {
    const [timelineItems, setTimelineItems] = useState([]);
    const [filteredItems, setFilteredItems] = useState([]);
    const [searchTerm, setSearchTerm] = useState([]);

    function filterEvents(search) {
        setSearchTerm(search)
        if (!search) {
            setFilteredItems(timelineItems);
        } else {
            setFilteredItems(timelineItems.filter(item => {
                return search ? Object.values(item).some(value => value.toString().toLowerCase().includes(search.toLowerCase())) : true;
            }));
        }
    }

    const customizedOpposite = (item) => {
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

    const customizedMarker = (item) => {
        return (
            <div className='p-timeline-event-marker' style={{ border: "2px solid " + item.color }}></div>
        )
    }

    const customizedContent = (item) => {
        return (
            // <Card subTitle={item.date}>
            <Box
                alignItems="center"
                gap={4}
                p={1}
            >{item.prof}
                <p><small>{item.comment}</small> {item.file && <a href={item.file}  target="_blank" rel="noreferrer"> <i className="pi pi-eye"></i> </a> }</p></Box>
                
            // </Card>
        );
  };

    return (
        <div>
            <GoogleSheetData apiKey={apiKey} sheetId={sheetId} setTimelineItems={setTimelineItems} setFilteredItems={setFilteredItems} />
            <Container maxWidth="md">
            <Fab 
                style={style} 
                color="primary" 
                aria-label="add" 
                href="https://docs.google.com/forms/d/1kiJwewfxg4YWWBCrivs1ZGEyPwVKs4f79SM7Jo-btUE/edit" 
                target="_blank"
            >
                <AddIcon />
            </Fab>
            
            <TextField
                label="Busca"
                variant="outlined"
                fullWidth
                margin="normal"
                value={searchTerm}
                onChange={(e) => filterEvents(e.target.value)}
            />

            <Box
              display="flex"
              flexDirection="column"
              alignItems="center"
              justifyContent="center"
              minHeight="100vh"
            >
                <div className="card">
                    {timelineItems.length > 0 ? (
                        <PrimeTimeline value={filteredItems ? filteredItems : timelineItems} opposite={customizedOpposite} marker={customizedMarker} content={customizedContent} />
                    ) : (
                        <CircularProgress />
                    )}
                </div>
            </Box>
            </Container>
        </div>
    );
};

export default Timeline;