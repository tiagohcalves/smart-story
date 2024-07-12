// src/components/GoogleSheetData.js
import { useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import axios from 'axios';
import { RANGE } from '../config';

const GoogleSheetData = ({ apiKey, sheetId, setTimelineItems }) => {
  const navigate = useNavigate();

  useEffect(() => {
    const fetchData = async () => {
      if (apiKey || sheetId) {
        const result = await axios.get(
          `https://sheets.googleapis.com/v4/spreadsheets/${sheetId}/values/${RANGE}?key=${apiKey}`
        );
        const data = result.data.values.map((row, index) => ({
          title: row[2],
          cardTitle: row[2],
          cardSubtitle: row[3],
          cardDetailedText: row[6],
          media: {
            type: "IMAGE",
            source: {
              url: (row[4] === "" ? "https://as2.ftcdn.net/v2/jpg/02/29/53/11/1000_F_229531197_jmFcViuzXaYOQdoOK1qyg7uIGdnuKhpt.jpg" : row[4]),
            },
          },
        }));
        setTimelineItems(data);
      } else {
        navigate("/")
      }
    };
    fetchData();
  }, [apiKey, setTimelineItems]);

  return null;
};

export default GoogleSheetData;
