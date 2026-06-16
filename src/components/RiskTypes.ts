export interface RiskAssessment {
  url?: string;
  type: 'URL' | 'EMAIL';
  riskScore: number;
  threatLevel: 'LOW' | 'MEDIUM' | 'HIGH' | 'CRITICAL';
  reasons: string[];
  topFindings: string[];
  breakdown: {
    threatIntelligence?: 'PASS' | 'WARNING' | 'ALERT';
    brandAnalysis?: 'PASS' | 'WARNING' | 'ALERT';
    contextAnalysis?: 'PASS' | 'WARNING' | 'ALERT';
    correlation?: 'PASS' | 'WARNING' | 'ALERT';
    domainTrust?: 'PASS' | 'WARNING' | 'ALERT';
    reputation?: 'PASS' | 'WARNING' | 'ALERT';
    classification?: string;
    modelConfidence?: string;
    threatLevel?: string;
  };
  technicalDetails: {
    aiScore?: number;
    brandScore?: number;
    contextScore?: number;
    correlationScore?: number;
    domainTrustScore?: number;
    reputationScore?: number;
    finalRisk: number;
  };
  campaign?: {
    brand: string;
    relatedEvents: number;
    campaignRisk: number;
  };
}
