import { IApiProvider } from '../../core/interfaces/IApiProvider';

export class BackendApiProvider implements IApiProvider {
  private baseUrl: string;

  constructor(baseUrl: string = 'http://localhost:8000') {
    this.baseUrl = baseUrl;
  }

async analyzeEmail(emailText: string): Promise<number | null> {
  try {
    console.log("[MIRAGE] Sending email request");

    const response = await fetch(`${this.baseUrl}/analyze-email`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ email_text: emailText }),
    });

    console.log("[MIRAGE] Fetch completed");

    if (!response.ok) {
      console.log("[MIRAGE] Response status:", response.status);
      throw new Error('API Response not ok');
    }

    const data = await response.json();

    console.log("[MIRAGE] JSON parsed");

    return data.risk_score;
  } catch (e) {
    console.error("[MIRAGE] Email API Analysis Failed:", e);
    return null;
  }
}

  async analyzeUrl(url: string): Promise<number | null> {
    try {
      const response = await fetch(`${this.baseUrl}/analyze-url`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ url }),
      });
      if (!response.ok) throw new Error('API Response not ok');
      const data = await response.json();
      return data.risk_score;
    } catch (e) {
      console.error('[MIRAGE] URL API Analysis Failed:', e);
      return null;
    }
  }
}
