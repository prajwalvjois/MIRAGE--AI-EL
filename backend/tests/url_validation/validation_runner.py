import sys
import os
import json
from dataclasses import dataclass, asdict
from typing import List, Dict

sys.path.append(os.path.join(os.path.dirname(__file__), "../.."))
from backend.factory.url_intelligence_factory import UrlIntelligenceFactory

@dataclass
class UrlAnalysisDebugResult:
    url: str
    ai_score: float
    threat_intelligence_score: float
    brand_score: float
    context_score: float
    correlation_score: float
    domain_trust_score: float
    final_risk: float
    reasons: List[str]

def load_urls(filename: str) -> List[str]:
    path = os.path.join(os.path.dirname(__file__), filename)
    if not os.path.exists(path):
        return []
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)

def run_validation():
    service = UrlIntelligenceFactory.get_service()
    
    datasets = {
        "SAFE URLS": "safe_urls.json",
        "SUSPICIOUS URLS": "suspicious_urls.json",
        "MALICIOUS URLS": "malicious_urls.json",
        "CAMPAIGN URLS": "campaign_urls.json"
    }
    
    reports = {}
    metrics = {}
    regression_findings = []
    
    for name, filename in datasets.items():
        urls = load_urls(filename)
        results = []
        risks = []
        
        for url in urls:
            try:
                assessment = service.analyze(url)
                
                ti_score = 1.0 if "Known malicious domain" in assessment.reasons else 0.0
                
                res = UrlAnalysisDebugResult(
                    url=url,
                    ai_score=assessment.ai_score,
                    threat_intelligence_score=ti_score,
                    brand_score=assessment.brand_score,
                    context_score=assessment.context_score,
                    correlation_score=assessment.correlation_score,
                    domain_trust_score=assessment.domain_trust_score,
                    final_risk=assessment.final_risk,
                    reasons=assessment.reasons
                )
                results.append(res)
                risks.append(res.final_risk)
                
                if name == "SAFE URLS" and res.final_risk > 0.5:
                    regression_findings.append({
                        "url": url,
                        "category": name,
                        "risk": res.final_risk,
                        "reasons": res.reasons
                    })
                elif name == "SUSPICIOUS URLS" and res.final_risk < 0.5:
                    regression_findings.append({
                        "url": url,
                        "category": name,
                        "risk": res.final_risk,
                        "reasons": res.reasons
                    })
            except Exception as e:
                print(f"Error analyzing {url}: {e}")
        
        reports[name] = [asdict(r) for r in results]
        
        if risks:
            avg_risk = sum(risks) / len(risks)
            high_risk = max(risks)
            low_risk = min(risks)
        else:
            avg_risk = 0.0
            high_risk = 0.0
            low_risk = 0.0
            
        metrics[name] = {
            "Average Risk": avg_risk,
        }
        if name != "CAMPAIGN URLS":
            metrics[name]["Highest Risk"] = high_risk
            metrics[name]["Lowest Risk"] = low_risk
        else:
            # Simple placeholder for campaigns detected
            metrics[name]["Campaigns Detected"] = 1 if len(risks) > 0 else 0

    output_dir = os.path.join(os.path.dirname(__file__), "output")
    os.makedirs(output_dir, exist_ok=True)
    
    # Save JSON report
    report_data = {
        "metrics": metrics,
        "regression_findings": regression_findings,
        "reports": reports
    }
    with open(os.path.join(output_dir, "validation_report.json"), "w", encoding="utf-8") as f:
        json.dump(report_data, f, indent=2)
        
    # Save TXT report
    with open(os.path.join(output_dir, "validation_report.txt"), "w", encoding="utf-8") as f:
        f.write("=== MIRAGE URL VALIDATION REPORT ===\n\n")
        
        f.write("--- SUMMARY METRICS ---\n")
        for name in datasets.keys():
            f.write(f"\n{name}\n")
            for k, v in metrics[name].items():
                if isinstance(v, float):
                    f.write(f"{k}: {v:.4f}\n")
                else:
                    f.write(f"{k}: {v}\n")
        
        f.write("\n--- REGRESSION FINDINGS ---\n")
        if not regression_findings:
            f.write("No regressions found.\n")
        else:
            for r in regression_findings:
                f.write(f"Category: {r['category']} | URL: {r['url']} | Final Risk: {r['risk']:.4f}\n")
                f.write(f"Reasons: {', '.join(r['reasons'])}\n")
                f.write("\n")
                
        f.write("\n--- DETAILED RESULTS ---\n")
        for name in datasets.keys():
            f.write(f"\n=== {name} ===\n")
            for r in reports[name]:
                f.write(f"URL: {r['url']}\n")
                f.write(f"AI Score: {r['ai_score']:.4f}\n")
                f.write(f"Threat Intelligence Score: {r['threat_intelligence_score']:.4f}\n")
                f.write(f"Brand Score: {r['brand_score']:.4f}\n")
                f.write(f"Context Score: {r['context_score']:.4f}\n")
                f.write(f"Correlation Score: {r['correlation_score']:.4f}\n")
                f.write(f"Domain Trust Score: {r['domain_trust_score']:.4f}\n")
                f.write(f"Final Risk: {r['final_risk']:.4f}\n")
                f.write("Reasons:\n")
                if not r['reasons']:
                    f.write("  - None\n")
                for reason in r['reasons']:
                    f.write(f"  - {reason}\n")
                f.write("\n")

if __name__ == "__main__":
    run_validation()
