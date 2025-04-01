
// server.js
const express = require('express');
const fs = require('fs');
const path = require('path');
const axios = require('axios');
const app = express();
const port = 3000;

// Insecure direct configuration loading
const apiKey = process.env.API_KEY || 'ey1234secretapikeyhere5678';
const backendUrl = process.env.BACKEND_URL || 'http://backend-service:5000';
const adminPassword = process.env.ADMIN_PASSWORD || 'd3fault_adm1n_p@ss';

// Vulnerable to path traversal
app.get('/read-file', (req, res) => {
  const filename = req.query.file;
  fs.readFile(filename, 'utf8', (err, data) => {
    if (err) {
      return res.status(500).send('Error reading file');
    }
    res.send(data);
  });
});

// Insecure admin endpoint with hardcoded credential check
app.get('/admin', (req, res) => {
  const password = req.query.password;
  if (password === adminPassword) {
    // FLAG hidden in admin page
    res.send(`
      <h1>Admin Panel</h1>
      <p>Welcome, admin!</p>
      <p>Server info: ${JSON.stringify(process.env)}</p>
      <p>Secret flag: FLAG{admin_portal_access}</p>
    `);
  } else {
    res.status(403).send('Access denied');
  }
});

// Proxy to backend with exposed API key
app.get('/api/:path', (req, res) => {
  const path = req.params.path;
  axios.get(`${backendUrl}/${path}`, {
    headers: {
      'Authorization': `Bearer ${apiKey}`
    }
  })
  .then(response => {
    res.json(response.data);
  })
  .catch(error => {
    res.status(500).json({ error: error.message });
  });
});

// Basic frontend
app.get('/', (req, res) => {
  res.send(`
    <!DOCTYPE html>
    <html>
    <head>
      <title>CTF Challenge</title>
    </head>
    <body>
      <h1>Welcome to the Vulnerable App</h1>
      <p>This application has multiple vulnerabilities. Can you find them all?</p>
      <!-- Note: Remove before production. Admin access for user admin at /api/login with password "${adminPassword}. Only in backend api!" -->
      <div id="content"></div>
      <script>
        // Vulnerable to XSS
        const urlParams = new URLSearchParams(window.location.search);
        const message = urlParams.get('message');
        if (message) {
          document.getElementById('content').innerHTML = message;
        }

        // Hidden flag in JavaScript
        function checkFlag() {
          return "FLAG{client_side_javascript_leak}";
        }
      </script>
    </body>
    </html>
  `);
});

app.listen(port, () => {
  console.log(`Frontend app listening at http://localhost:${port}`);
});
