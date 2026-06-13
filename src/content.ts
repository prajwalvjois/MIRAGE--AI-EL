import { GmailExtractor } from './providers/email/GmailExtractor';
import { BackendApiProvider } from './providers/api/BackendApiProvider';

const extractor = new GmailExtractor();
const apiProvider = new BackendApiProvider();
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
        
        const riskScore = await apiProvider.analyzeEmail(text);
        console.log(`[MIRAGE] Email Risk Score: ${riskScore}`);
      }
    }
  }, 2000);
}

