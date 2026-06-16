const fetch = require('node-fetch');
fetch('http://127.0.0.1:8000/analyze-email', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({ email_text: "test" })
}).then(res => res.text()).then(console.log).catch(console.error);
