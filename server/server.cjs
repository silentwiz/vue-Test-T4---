const express = require('express');
const cors = require('cors');
const bodyParser = require('body-parser');
const fs = require('fs');
const path = require('path');
const { format } = require('@fast-csv/format');
const { spawn } = require('child_process');

const app = express();
const PORT = 3001;

app.use(cors());
app.use(bodyParser.json());

app.post('/api/submit', (req, res) => {
  const data = req.body;

  if (Array.isArray(data.interfaces)) {
    data.interfaces = data.interfaces.join(';');
  }

  const filePath = path.join(__dirname, 'answers.csv');
  const fileExists = fs.existsSync(filePath);
  const headers = Object.keys(data);
  const ws = fs.createWriteStream(filePath, { flags: 'a' });
  const csvStream = format({
    headers: !fileExists ? headers : false,
    rowDelimiter: '\r\n',
    includeEndRowDelimiter: true,
  });

  csvStream.pipe(ws);
  csvStream.write(data);
  csvStream.end();

  ws.on('finish', () => {
    res.json({ success: true });
  });
});

app.get('/api/results', (req, res) => {
  const pythonProcess = spawn('python3', [path.join(__dirname, 'pyth_plot_ge.py')]);

  let pythonOutput = '';

  pythonProcess.stdout.on('data', (data) => {
    pythonOutput += data.toString();
  });

  pythonProcess.stderr.on('data', (data) => {
    console.error(`Python script error: ${data}`);
  });

  pythonProcess.on('close', (code) => {
    console.log(`Python script exited with code ${code}`);
    try {
      const jsonData = JSON.parse(pythonOutput);
      res.json(jsonData);
    } catch (error) {
      res.status(500).json({ error: 'Failed to parse Python script output' });
    }
  });
});

app.get('/api/data', (req, res) => {
  const csvFilePath = path.join(__dirname, 'answers.csv');

  fs.readFile(csvFilePath, 'utf8', (err, data) => {
    if (err) {
      console.error('Error reading CSV file:', err);
      return res.status(500).json({ error: 'Failed to read data file.' });
    }

    const lines = data.trim().split(/\r?\n/);
    if (lines.length < 2) {
      return res.json([]);
    }
    const headers = lines[0].split(',');
    const jsonData = lines.slice(1).map(line => {
      const values = line.split(',');
      const entry = {};
      headers.forEach((header, index) => {
        entry[header] = values[index];
      });
      return entry;
    });

    res.json(jsonData);
  });
});

app.listen(PORT, () => {
  console.log(`Server listening at http://localhost:${PORT}`);
});