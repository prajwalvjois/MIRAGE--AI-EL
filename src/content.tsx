import React, { useState, useEffect } from 'react';
import { createRoot } from 'react-dom/client';
import { GmailExtractor } from './providers/email/GmailExtractor';
import { ChromeProvider } from './providers/browser/ChromeProvider';
import { AlertTriangle, ShieldAlert, X } from 'lucide-react';
import './index.css';

const extractor = new GmailExtractor();
const browserProvider = new ChromeProvider();

// UI Components for warnings
const MediumRiskBanner = ({ score, dismiss }: { score: number, dismiss: () => void }) => (
  <div className="fixed top-4 right-4 z-[999999] bg-yellow-50 border border-yellow-300 shadow-lg rounded-lg p-3 flex items-start gap-3 w-80 font-sans">
    <AlertTriangle className="w-5 h-5 text-yellow-600 shrink-0 mt-0.5" />
    <div className="flex-1">
      <h3 className="text-yellow-800 font-bold text-sm mb-1 uppercase tracking-tight">MIRAGE WARNING</h3>
      <p className="text-yellow-700 text-xs mb-2">Potentially suspicious content detected.<br/>Risk Score: {(score * 100).toFixed(0)}%</p>
      <button className="text-xs bg-yellow-200 hover:bg-yellow-300 text-yellow-800 px-2 py-1 rounded font-medium transition-colors" onClick={() => {
        // Open popup is not possible automatically from content script easily in all browsers,
        // but we can just say "View Analysis in Extension".
        alert("Please open the MIRAGE extension popup to view full analysis.");
      }}>View Analysis</button>
    </div>
    <button onClick={dismiss} className="text-yellow-500 hover:text-yellow-700 p-1"><X className="w-4 h-4" /></button>
  </div>
);

const HighRiskBanner = ({ score, dismiss }: { score: number, dismiss: () => void }) => (
  <div className="fixed top-0 left-0 right-0 z-[999999] bg-orange-600 text-white shadow-xl px-4 py-3 flex items-center justify-between font-sans">
    <div className="flex items-center gap-3">
      <ShieldAlert className="w-6 h-6 text-orange-100" />
      <div>
        <h3 className="font-bold text-sm tracking-widest uppercase">⚠ HIGH RISK</h3>
        <p className="text-orange-100 text-xs">Risk Score: {(score * 100).toFixed(0)}%. Brand impersonation or high risk factors detected.</p>
      </div>
    </div>
    <div className="flex items-center gap-2">
      <button className="text-xs bg-white text-orange-700 hover:bg-orange-50 px-3 py-1.5 rounded font-bold transition-colors" onClick={() => {
        alert("Please open the MIRAGE extension popup to view full analysis.");
      }}>View Details</button>
      <button onClick={dismiss} className="text-xs bg-orange-700 hover:bg-orange-800 text-white px-3 py-1.5 rounded font-medium transition-colors">Dismiss</button>
    </div>
  </div>
);

const CriticalRiskPage = ({ score, goBack, proceed }: { score: number, goBack: () => void, proceed: () => void }) => (
  <div className="fixed inset-0 z-[9999999] bg-red-600 flex flex-col items-center justify-center font-sans text-center px-4">
    <div className="bg-white rounded-2xl shadow-2xl max-w-lg w-full p-8">
      <ShieldAlert className="w-16 h-16 text-red-600 mx-auto mb-4" />
      <h1 className="text-3xl font-black text-slate-900 mb-2">🚨 DANGEROUS WEBSITE</h1>
      <p className="text-slate-600 mb-6">Known malicious domain or critical threat detected.</p>
      
      <div className="bg-red-50 border border-red-100 rounded-xl p-4 mb-8 flex divide-x divide-red-200">
        <div className="flex-1 px-2">
          <div className="text-xs font-bold text-red-500 uppercase tracking-widest mb-1">Source</div>
          <div className="text-lg font-bold text-red-700">Threat Intelligence</div>
        </div>
        <div className="flex-1 px-2">
          <div className="text-xs font-bold text-red-500 uppercase tracking-widest mb-1">Risk Score</div>
          <div className="text-lg font-bold text-red-700">{(score * 100).toFixed(0)}%</div>
        </div>
      </div>

      <div className="flex flex-col gap-3">
        <button onClick={goBack} className="w-full bg-red-600 hover:bg-red-700 text-white font-bold py-3 px-4 rounded-xl transition-colors">
          Go Back (Recommended)
        </button>
        <button onClick={proceed} className="w-full bg-slate-100 hover:bg-slate-200 text-slate-600 font-bold py-3 px-4 rounded-xl transition-colors">
          Proceed Anyway
        </button>
      </div>
    </div>
  </div>
);

const WarningApp = ({ finalRisk, reasons }: { finalRisk: number, reasons: string[] }) => {
  const [dismissed, setDismissed] = useState(false);

  if (dismissed) return null;

  const isCritical = finalRisk >= 1.0 || reasons.includes("Known malicious domain");
  const isHigh = finalRisk >= 0.70 && !isCritical;
  const isMedium = finalRisk >= 0.30 && finalRisk < 0.70;

  if (isCritical) {
    return <CriticalRiskPage score={finalRisk} goBack={() => window.history.back()} proceed={() => setDismissed(true)} />;
  }
  
  if (isHigh) {
    return <HighRiskBanner score={finalRisk} dismiss={() => setDismissed(true)} />;
  }
  
  if (isMedium) {
    return <MediumRiskBanner score={finalRisk} dismiss={() => setDismissed(true)} />;
  }

  return null;
};

// URL Analysis logic for all pages
const analyzeUrl = async () => {
  try {
    const res = await fetch('http://127.0.0.1:8000/analyze-url', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ url: window.location.href })
    });
    if (res.ok) {
      const data = await res.json();
      const finalRisk = data.risk_score ?? 0;
      if (finalRisk >= 0.3) {
        // Inject Warning UI
        const container = document.createElement('div');
        container.id = 'mirage-warning-container';
        document.body.appendChild(container);
        const root = createRoot(container);
        root.render(<WarningApp finalRisk={finalRisk} reasons={data.reasons || []} />);
      }
    }
  } catch (e) {
    console.error("[MIRAGE] Error analyzing URL:", e);
  }
};

// Run URL Analysis on load
analyzeUrl();

// Email Analysis Logic
let lastExtractedText: string | null = null;

chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
  if (request.type === 'GET_EMAIL_BODY') {
    sendResponse(lastExtractedText);
  }
});

if (extractor.isTargetPage(window.location.href)) {
  setInterval(async () => {
    if (extractor.isEmailOpen()) {
      const text = extractor.extractBody();
      if (text && text !== lastExtractedText) {
        lastExtractedText = text;
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

