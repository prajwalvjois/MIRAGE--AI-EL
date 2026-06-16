import { ChromeProvider } from './providers/browser/ChromeProvider';
import { BackendApiProvider } from './providers/api/BackendApiProvider';

const browserProvider = new ChromeProvider();
const apiProvider = new BackendApiProvider();

browserProvider.onUrlChanged(async (tabId, newUrl) => {
  console.log(`[MIRAGE] URL Change Detected -> Tab ${tabId}: ${newUrl}`);
  
  try {
    const response = await fetch('http://127.0.0.1:8000/analyze-url', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ url: newUrl }),
    });
    if (response.ok) {
      const data = await response.json();
      const finalRisk = data.risk_score ?? 0;
      console.log(`[MIRAGE] URL Risk Score for ${newUrl}: ${finalRisk}`);
      
      // Inject if needed
      if (finalRisk >= 0.3) {
        chrome.tabs.sendMessage(tabId, {
          type: 'SHOW_WARNING',
          payload: {
            finalRisk,
            reasons: data.reasons || []
          }
        });
      }
    }
  } catch (e) {
    console.error("[MIRAGE] Error in URL Change Analysis:", e);
  }
});

browserProvider.onMessage((message, sender, sendResponse) => {
  if (message.type === 'ANALYZE_EMAIL' && message.payload) {
    // Process async work and return true to indicate we will sendResponse asynchronously
    apiProvider.analyzeEmail(message.payload)
      .then(riskScore => {
        sendResponse(riskScore);
      })
      .catch(error => {
        console.error("[MIRAGE] Background API Error:", error);
        sendResponse(null);
      });
    return true; // Needed for async sendResponse
  }
});

console.log("[MIRAGE] Background Service Worker Initialized.");

