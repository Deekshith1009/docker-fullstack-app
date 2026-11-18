const express = require('express');
const path = require('path');

const app = express();
const PORT = process.env.PORT || 3000;
const BACKEND_URL = process.env.BACKEND_URL || 'http://localhost:5000';

app.use(express.urlencoded({ extended: true }));
app.use(express.static(path.join(__dirname, 'public')));

app.post('/submit', async (req, res) => {
  try {
    const response = await fetch(`${BACKEND_URL}/submittodoitem`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
      body: new URLSearchParams(req.body),
    });
    const data = await response.json();
    const text = data.message || data.error || 'Unknown response';
    res.status(response.status).send(`<h2>${text}</h2><a href="/">Back to form</a>`);
  } catch (err) {
    res.status(502).send('<h2>Could not reach the backend</h2><a href="/">Back to form</a>');
  }
});

app.listen(PORT, '0.0.0.0', () => {
  console.log(`Frontend running on port ${PORT}`);
});