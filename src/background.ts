import { ChromeProvider } from './providers/browser/ChromeProvider';
import { BackendApiProvider } from './providers/api/BackendApiProvider';

const browserProvider = new ChromeProvider();
const apiProvider = new BackendApiProvider();

browserProvider.onUrlChanged(async (tabId, newUrl) => {
  console.log(`[MIRAGE] URL Change Detected -> Tab ${tabId}: ${newUrl}`);
  const riskScore = await apiProvider.analyzeUrl(newUrl);
  console.log(`[MIRAGE] URL Risk Score for ${newUrl}: ${riskScore}`);
});

console.log("[MIRAGE] Background Service Worker Initialized.");

