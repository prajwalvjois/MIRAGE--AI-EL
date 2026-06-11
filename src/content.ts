import { GmailExtractor } from './providers/email/GmailExtractor';

const extractor = new GmailExtractor();
let lastExtractedText: string | null = null;

if (extractor.isTargetPage(window.location.href)) {
  console.log("[MIRAGE] Stage 1 Validating: Gmail Detected.");

  // For MVP feasibility, use a simple poll to wait for asynchronous body loading
  setInterval(() => {
    if (extractor.isEmailOpen()) {
      const text = extractor.extractBody();
      if (text && text !== lastExtractedText) {
        lastExtractedText = text;
        console.log("[MIRAGE] Extracted Email Body Snapshot:");
        console.log(text.substring(0, 150) + "...");
        console.log("------------------------");
      }
    }
  }, 2000);
}
