import { ChromeProvider } from './providers/browser/ChromeProvider';

const browserProvider = new ChromeProvider();

browserProvider.onUrlChanged((tabId, newUrl) => {
  console.log(`[MIRAGE] URL Change Detected -> Tab ${tabId}: ${newUrl}`);
});

console.log("[MIRAGE] Background Service Worker Initialized.");
