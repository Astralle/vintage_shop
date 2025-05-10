// server_inv.js
const express    = require('express');
const bodyParser = require('body-parser');
const fs         = require('fs');
const path       = require('path');

const app = express();
const PORT = process.env.PORT || 3000;
const DATA_FILE = path.join(__dirname, 'data', 'featured.json');

// parse JSON bodies
app.use(bodyParser.json());

// serve front-end assets
app.use(express.static(path.join(__dirname, 'public')));

// Utility to read/write the JSON file
function readData() {
  return JSON.parse(fs.readFileSync(DATA_FILE, 'utf8'));
}
function writeData(data) {
  fs.writeFileSync(DATA_FILE, JSON.stringify(data, null, 2), 'utf8');
}

// -- API ROUTES --

// GET all items
app.get('/api/items', (req, res) => {
  try {
    res.json(readData());
  } catch (e) {
    res.status(500).json({ error: 'Unable to read data.' });
  }
});

// POST (add) a new item
app.post('/api/items', (req, res) => {
  const items = readData();
  const newItem = req.body;
  // generate a unique ID (e.g. timestamp)
  newItem.id = Date.now();
  items.push(newItem);
  writeData(items);
  res.status(201).json(newItem);
});

// PUT (update) an existing item
app.put('/api/items/:id', (req, res) => {
  const id = parseInt(req.params.id, 10);
  let items = readData();
  const index = items.findIndex(i => i.id === id);
  if (index === -1) return res.status(404).json({ error: 'Not found.' });
  // merge changes
  items[index] = { ...items[index], ...req.body, id };
  writeData(items);
  res.json(items[index]);
});

// DELETE an item
app.delete('/api/items/:id', (req, res) => {
  const id = parseInt(req.params.id, 10);
  let items = readData();
  const newItems = items.filter(i => i.id !== id);
  if (newItems.length === items.length) {
    return res.status(404).json({ error: 'Not found.' });
  }
  writeData(newItems);
  res.status(204).end();
});

// start server
app.listen(PORT, () => console.log(`Server listening on http://localhost:${PORT}`));
