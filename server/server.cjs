const express = require('express')
const cors = require('cors')
const bodyParser = require('body-parser')
const fs = require('fs')
const { format } = require('@fast-csv/format')
const { spawn } = require('child_process')

const app = express()
const PORT = 3001

app.use(cors())
app.use(bodyParser.json())

app.post('/api/submit', (req, res) => {
  const data = req.body
  const filePath = 'answers.csv'
  const fileExists = fs.existsSync(filePath)
  const headers = Object.keys(data)
  const ws = fs.createWriteStream(filePath, { flags: 'a' })
  const csvStream = format({
    headers: !fileExists ? headers : false,
    rowDelimiter: '\r\n',
    includeEndRowDelimiter: true,
  })

  csvStream.pipe(ws)
  csvStream.write(data)
  csvStream.end()

  ws.on('finish', () => {
    res.json({ success: true })
  })
})

app.get('/run-python-file', (req, res) => {
  const pythonProcess = spawn('python3', ['plot_ver2.py'])

  let pythonOutput = ''

  pythonProcess.stdout.on('data', (data) => {
    pythonOutput += data.toString()
  })

  pythonProcess.stderr.on('data', (data) => {
    console.error(`Python script error: ${data}`)
  })

  pythonProcess.on('close', (code) => {
    console.log(`Python script exited with code ${code}`)
    try {
      const jsonData = JSON.parse(pythonOutput)
      res.json(jsonData)
    } catch (error) {
      res.status(500).json({ error: 'Failed to parse Python script output' })
    }
  })
})

app.listen(PORT, () => {
  console.log(`Server running at http://localhost:${PORT}`)
})
