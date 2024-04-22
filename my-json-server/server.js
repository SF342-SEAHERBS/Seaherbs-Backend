const express = require('express');
const fs = require('fs');
const cors = require('cors');

const app = express();
const PORT = process.env.PORT || 3005; // Use the provided port or default to 3000

// Serve static files from the public directory (optional)
app.use(express.static('public'));
app.use(cors());

// Read JSON data from dataset_3.json synchronously when the server starts
const jsonData = JSON.parse(fs.readFileSync('dataset_7.json', 'utf8'));

// Serve your JSON data at the /api/data endpoint
app.get('/api/data', (req, res) => {
    res.json(jsonData);
});

// Serve your JSON data at the /data endpoint
app.get('/data', (req, res) => {
    fs.readFile('dataset_7.json', 'utf8', (err, data) => {
        if (err) {
            console.error('Error reading JSON file:', err);
            res.status(500).send('Internal Server Error');
            return;
        }
        res.json(JSON.parse(data));
    });
});

// Start the server
app.listen(PORT, () => {
    console.log(`Server is running on http://localhost:${PORT}`);
});
