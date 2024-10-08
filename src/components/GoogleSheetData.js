// src/components/GoogleSheetData.js
import { useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import axios from 'axios';
import { RANGE } from '../config';

const GoogleSheetData = ({ apiKey, sheetId, setTimelineItems, setFilteredItems }) => {
  const navigate = useNavigate();

  const rowIndex = {
    "TIMESTAMP": 0,
    "DATE": 1,
    "TYPE": 2,
    "PROFESSIONAL": 3,
    "FILE": 4,
    "URL": 5,
    "COMMENT": 6
  }

  const colorMap = {
    "Consulta":	"#FF5733",
    "Pedido":	"#33FF57",
    "Exame":	"#3357FF",
    "Evento":	"#FF33A1",
    "Receita":	"#FFB733",
    "Encaminhamento":	"#33FFF2",
    "Diagnóstico":	"#D433FF"
  }

  function toDate(dateString) {
    var parts = dateString.split('/');
    return new Date(parts[2], parts[1] - 1, parts[0]); 
  }

  useEffect(() => {
    const fetchData = async () => {
      if (apiKey || sheetId) {
        const result = await axios.get(
          `https://sheets.googleapis.com/v4/spreadsheets/${sheetId}/values/${RANGE}?key=${apiKey}`
        );
        const data = result.data.values.map((row, index) => ({
          // title: row[2],
          // cardTitle: row[2],
          // cardSubtitle: row[3],
          // cardDetailedText: row[6],
          // media: {
          //   type: "IMAGE",
          //   source: {
          //     url: (row[4] === "" ? "https://as2.ftcdn.net/v2/jpg/02/29/53/11/1000_F_229531197_jmFcViuzXaYOQdoOK1qyg7uIGdnuKhpt.jpg" : row[4]),
          //   },
          // },
          date: row[rowIndex["DATE"]],
          dt: toDate(row[rowIndex["DATE"]]),
          type: row[rowIndex["TYPE"]],
          prof: row[rowIndex["PROFESSIONAL"]],
          file: row[rowIndex["FILE"]],
          comment: row[rowIndex["COMMENT"]] ?? "",
          color: colorMap[row[rowIndex["TYPE"]]] ?? "#CCCCCC"
        })).sort((a, b) => a["dt"] > b["dt"] ? -1 : (a["dt"] < b["dt"] ? 1 : 0));
        setTimelineItems(data);
        setFilteredItems(data);
      } else {
        navigate("/smart-story")
      }
    };
    fetchData();
  }, [apiKey, setTimelineItems]);

  return null;
};

export default GoogleSheetData;
