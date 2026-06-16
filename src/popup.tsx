import React, { useState } from 'react';
import { AlertTriangle, ShieldCheck, ChevronDown, ChevronUp, Info, Activity } from 'lucide-react';
import { RiskAssessment } from './components/RiskTypes';
import './index.css';
import { createRoot } from 'react-dom/client';

const ThreatLevelBadge = ({ level }: { level: string }) => {
  const colors = {
    LOW: 'bg-green-100 text-green-800 border-green-200',
    MEDIUM: 'bg-yellow-100 text-yellow-800 border-yellow-200',
    HIGH: 'bg-orange-100 text-orange-800 border-orange-200',
    CRITICAL: 'bg-red-100 text-red-800 border-red-200'
  };
  const color = colors[level as keyof typeof colors] || colors.LOW;
  return (
    <span className={`px-2 py-1 text-xs font-bold rounded-md border ${color}`}>
      {level}
    </span>
  );
};

const RiskScoreCard = ({ type, score, level }: { type: 'URL' | 'EMAIL', score: number, level: string }) => {
  return (
    <div className="bg-white p-4 rounded-lg shadow-sm border border-slate-200 mb-4 flex items-center justify-between">
      <div>
        <h2 className="text-lg font-bold text-slate-800">{type === 'URL' ? 'URL Analysis' : 'Email Analysis'}</h2>
        <div className="mt-1 flex items-center gap-2">
          <span className="text-sm text-slate-500">Risk Score:</span>
          <span className="font-mono font-bold text-slate-700">{(score * 100).toFixed(0)}%</span>
        </div>
      </div>
      <div>
        <ThreatLevelBadge level={level} />
      </div>
    </div>
  );
};

const ReasonList = ({ reasons }: { reasons: string[] }) => {
  if (!reasons || reasons.length === 0) return null;
  return (
    <div className="mb-4">
      <h3 className="text-sm font-semibold text-slate-800 mb-2 uppercase tracking-wide">Top Findings</h3>
      <ul className="space-y-2">
        {reasons.map((r, i) => (
          <li key={i} className="flex items-start gap-2 text-sm text-slate-600 bg-slate-50 p-2 rounded border border-slate-100">
            <AlertTriangle className="w-4 h-4 text-amber-500 shrink-0 mt-0.5" />
            <span>{r}</span>
          </li>
        ))}
      </ul>
    </div>
  );
};

const AnalysisBreakdownPanel = ({ breakdown }: { breakdown: Record<string, string> }) => {
  if (!breakdown) return null;
  const labels: Record<string, string> = {
    threatIntelligence: 'Threat Intelligence',
    brandAnalysis: 'Brand Analysis',
    contextAnalysis: 'Context Analysis',
    correlation: 'Correlation',
    domainTrust: 'Domain Trust',
    reputation: 'Reputation',
    classification: 'Classification',
    modelConfidence: 'Model Confidence',
    threatLevel: 'Threat Level'
  };

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'PASS': case 'LOW': return 'text-green-600';
      case 'WARNING': case 'MEDIUM': return 'text-amber-600';
      case 'ALERT': return 'text-red-600';
      case 'HIGH': return 'text-orange-600';
      case 'CRITICAL': return 'text-red-700 font-black';
      case 'PHISHING': case 'MALICIOUS': return 'text-red-600 font-bold';
      case 'SAFE': return 'text-green-600';
      default: return 'text-slate-600';
    }
  };

  return (
    <div className="mb-4">
      <h3 className="text-sm font-semibold text-slate-800 mb-2 uppercase tracking-wide">Detection Breakdown</h3>
      <div className="bg-white rounded-lg border border-slate-200 overflow-hidden divide-y divide-slate-100">
        {Object.entries(breakdown).map(([k, v]) => (
          <div key={k} className="flex justify-between items-center px-3 py-2">
            <span className="text-sm text-slate-600">{labels[k] || k}</span>
            <span className={`text-xs font-bold ${getStatusColor(v)}`}>{v}</span>
          </div>
        ))}
      </div>
    </div>
  );
};

const CampaignDetectionCard = ({ campaign }: { campaign: any }) => {
  if (!campaign) return null;
  return (
    <div className="mb-4 bg-indigo-50 border border-indigo-100 rounded-lg p-3">
      <div className="flex items-center gap-2 mb-2 text-indigo-800">
        <Activity className="w-4 h-4" />
        <h3 className="text-sm font-bold uppercase tracking-wide">Campaign Correlation</h3>
      </div>
      <div className="space-y-1 text-sm text-indigo-700">
        <div className="flex justify-between"><span>Target Brand:</span> <span className="font-medium">{campaign.brand}</span></div>
        <div className="flex justify-between"><span>Related Events:</span> <span className="font-medium">{campaign.relatedEvents}</span></div>
        <div className="flex justify-between"><span>Campaign Risk:</span> <span className="font-mono font-medium">{(campaign.campaignRisk * 100).toFixed(0)}%</span></div>
      </div>
    </div>
  );
};

const TechnicalDetailsAccordion = ({ details }: { details: Record<string, number> }) => {
  const [open, setOpen] = useState(false);
  if (!details) return null;

  return (
    <div className="mb-4 border border-slate-200 rounded-lg bg-white overflow-hidden">
      <button 
        onClick={() => setOpen(!open)}
        className="w-full flex justify-between items-center px-4 py-3 bg-slate-50 hover:bg-slate-100 transition-colors"
      >
        <div className="flex items-center gap-2 text-slate-700">
          <Info className="w-4 h-4" />
          <span className="text-sm font-semibold">Technical Details</span>
        </div>
        {open ? <ChevronUp className="w-4 h-4 text-slate-500" /> : <ChevronDown className="w-4 h-4 text-slate-500" />}
      </button>
      {open && (
        <div className="p-4 space-y-2 border-t border-slate-200">
          {Object.entries(details).map(([k, v]) => (
            <div key={k} className="flex justify-between items-center text-xs">
              <span className="text-slate-500 font-mono">{k}</span>
              <span className="text-slate-800 font-mono font-medium">{v.toFixed(4)}</span>
            </div>
          ))}
        </div>
      )}
    </div>
  );
};

const LoadingState = () => (
  <div className="flex flex-col items-center justify-center h-48 space-y-4">
    <div className="w-8 h-8 border-4 border-slate-200 border-t-indigo-600 rounded-full animate-spin"></div>
    <span className="text-sm text-slate-500 font-medium animate-pulse">Running MIRAGE Engine...</span>
  </div>
);

const ErrorState = ({ message }: { message: string }) => (
  <div className="bg-red-50 border border-red-200 rounded-lg p-4 text-center">
    <AlertTriangle className="w-8 h-8 text-red-500 mx-auto mb-2" />
    <h3 className="text-red-800 font-bold mb-1">Analysis Failed</h3>
    <p className="text-xs text-red-600">{message}</p>
  </div>
);

const PopupApp = () => {
  const [data, setData] = useState<RiskAssessment | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  React.useEffect(() => {
    // We will talk to background page or perform logic to get the current tab URL and query the API
    // Wait, the API endpoint is implemented in Python, we can hit it directly or via background.ts
    // Let's implement querying the background script.
    
    const analyzeCurrentTab = async () => {
      try {
        const [tab] = await chrome.tabs.query({ active: true, currentWindow: true });
        if (!tab || !tab.url) {
          throw new Error('No active tab or URL found');
        }

        let isEmail = false;
        let emailBody = null;
        if (tab.url.includes('mail.google.com')) {
          try {
            emailBody = await new Promise((resolve) => {
              chrome.tabs.sendMessage(tab.id as number, { type: 'GET_EMAIL_BODY' }, (res) => {
                resolve(res);
              });
            });
            if (emailBody) isEmail = true;
          } catch(e) {}
        }

        let res;
        let finalRisk = 0;
        let r: string[] = [];
        let riskData: any;

        if (isEmail) {
          res = await fetch('http://127.0.0.1:8000/analyze-email', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ body: emailBody })
          });
          if (!res.ok) throw new Error(`API error: ${res.status}`);
          riskData = await res.json();
          // The email backend returns {'risk_score': 0.8, 'classification': 'PHISHING', 'reasons': [...]} 
          // We map this safely
          finalRisk = riskData.risk_score ?? riskData.final_risk ?? 0;
          r = riskData.reasons ?? riskData.explanations ?? [];
        } else {
          res = await fetch('http://127.0.0.1:8000/analyze-url', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ url: tab.url })
          });
          if (!res.ok) throw new Error(`API error: ${res.status}`);
          riskData = await res.json();
          finalRisk = riskData.final_risk ?? 0;
          r = riskData.reasons ?? [];
        }
        let threatLevel: 'LOW' | 'MEDIUM' | 'HIGH' | 'CRITICAL' = 'LOW';
        if (finalRisk >= 1.0 || riskData.reasons?.includes("Known malicious domain")) {
          threatLevel = 'CRITICAL';
        } else if (finalRisk >= 0.7) {
          threatLevel = 'HIGH';
        } else if (finalRisk >= 0.3) {
          threatLevel = 'MEDIUM';
        }

        // Generate synthetic breakdown since backend doesn't output PASS/WARNING/ALERT directly
        // We do basic heuristics based on reasons.
        const has = (word: string) => r.some(x => x.toLowerCase().includes(word));
        
        setData({
          type: isEmail ? 'EMAIL' : 'URL',
          riskScore: finalRisk,
          threatLevel,
          topFindings: r.slice(0, 4), // TOP 4
          reasons: r,
          breakdown: isEmail ? {
             classification: riskData.classification || 'UNKNOWN',
             modelConfidence: riskData.confidence ? `${(riskData.confidence * 100).toFixed(0)}%` : 'N/A',
             threatLevel: threatLevel
          } : {
            threatIntelligence: has('known malicious') ? 'ALERT' : 'PASS',
            brandAnalysis: has('brand mismatch') || has('impersonation') ? 'ALERT' : 'PASS',
            contextAnalysis: has('login') || has('security') ? 'WARNING' : 'PASS',
            correlation: has('correlation') ? 'WARNING' : 'PASS',
            domainTrust: has('days') || has('short') || has('less than') ? (has('unavailable') ? 'WARNING' : 'ALERT') : 'PASS',
            reputation: has('low reputation') || has('rare') ? 'WARNING' : 'PASS'
          },
          technicalDetails: isEmail ? {
            finalRisk: finalRisk
          } : {
            aiScore: riskData.ai_score || 0,
            brandScore: riskData.brand_score || 0,
            contextScore: riskData.context_score || 0,
            correlationScore: riskData.correlation_score || 0,
            domainTrustScore: riskData.domain_trust_score || 0,
            reputationScore: riskData.reputation_score || 0,
            finalRisk: finalRisk
          }
        });
      } catch (err: any) {
        setError(err.message || 'Unknown error');
      } finally {
        setLoading(false);
      }
    };

    analyzeCurrentTab();
  }, []);

  return (
    <div className="w-full min-h-full p-4 flex flex-col font-sans">
      <div className="flex items-center gap-2 mb-4 pb-3 border-b border-slate-200">
        <ShieldCheck className="w-6 h-6 text-indigo-600" />
        <h1 className="text-xl font-black tracking-tight text-slate-800">MIRAGE</h1>
      </div>
      
      {loading && <LoadingState />}
      {error && <ErrorState message={error} />}
      {!loading && !error && data && (
        <div className="flex-1 overflow-y-auto pr-1 custom-scrollbar">
          <RiskScoreCard type={data.type} score={data.riskScore} level={data.threatLevel} />
          
          <div className="mb-6">
            <h3 className="text-xs uppercase tracking-wider font-bold text-slate-400 mb-2">Verdict Details</h3>
            <ReasonList reasons={data.reasons} />
          </div>

          <AnalysisBreakdownPanel breakdown={data.breakdown} />
          <TechnicalDetailsAccordion details={data.technicalDetails} />
          <CampaignDetectionCard campaign={data.campaign} />
        </div>
      )}
    </div>
  );
};

const root = createRoot(document.getElementById('root') as HTMLElement);
root.render(<PopupApp />);
