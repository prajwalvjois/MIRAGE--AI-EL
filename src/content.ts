import { GmailExtractor } from './providers/email/GmailExtractor';
import { ChromeProvider } from './providers/browser/ChromeProvider';

const extractor = new GmailExtractor();
const browserProvider = new ChromeProvider();
let lastExtractedText: string | null = null;

if (extractor.isTargetPage(window.location.href)) {
  console.log("[MIRAGE] Stage 2 Validating: Gmail Detected.");

  // For MVP feasibility, use a simple poll to wait for asynchronous body loading
  setInterval(async () => {
    if (extractor.isEmailOpen()) {
      const text = extractor.extractBody();
      if (text && text !== lastExtractedText) {
        lastExtractedText = text;
        console.log("[MIRAGE] Extracted Email Body Snapshot:");
        console.log(text.substring(0, 150) + "...");
        console.log("------------------------");
        
        console.log("[MIRAGE] Requesting Email Analysis...");
        try {
          const riskScore = await browserProvider.sendMessage<number>({
            type: 'ANALYZE_EMAIL',
            payload: text
          });
          console.log(`[MIRAGE] Email Risk Score: ${riskScore}`);
        } catch (e) {
          console.error("[MIRAGE] Error requesting analysis:", e);
        }
      }
    }
  }, 2000);
}

