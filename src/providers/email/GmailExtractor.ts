import { IEmailExtractor } from '../../core/interfaces/IEmailExtractor';

export class GmailExtractor implements IEmailExtractor {
  isTargetPage(url: string): boolean {
    return url.includes('mail.google.com');
  }

  isEmailOpen(): boolean {
    // Gmail uses the '.a3s.aiL' class for fully loaded email bodies
    return document.querySelector('.a3s.aiL') !== null;
  }

  extractBody(): string | null {
    const bodies = document.querySelectorAll('.a3s.aiL');
    if (bodies.length > 0) {
        // Return the last instance in the DOM tree, which is the expanded email in a thread
      const activeBody = bodies[bodies.length - 1] as HTMLElement;
      return activeBody.innerText?.trim() || null;
    }
    return null;
  }
}
