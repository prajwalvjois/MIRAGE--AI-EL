import { ChromeProvider } from './providers/browser/ChromeProvider';
import { BackendApiProvider } from './providers/api/BackendApiProvider';

const browserProvider = new ChromeProvider();
const apiProvider = new BackendApiProvider();

browserProvider.onUrlChanged(async (tabId, newUrl) => {
  console.log(`[MIRAGE] URL Change Detected -> Tab ${tabId}: ${newUrl}`);
  const riskScore = await apiProvider.analyzeUrl(newUrl);
  console.log(`[MIRAGE] URL Risk Score for ${newUrl}: ${riskScore}`);
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

