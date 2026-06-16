const fetch = require('node-fetch');

async function test() {
  try {
    const res = await fetch("http://localhost:8000/analyze-url", {
      method: "POST",
      headers: {"Content-Type": "application/json"},
      body: JSON.stringify({url: "chrome://newtab/"})
    });
    console.log("Status:", res.status);
    console.log("Result:", await res.json());
  } catch(e) {
    console.error("Fetch failed:", e);
  }
}
test();
