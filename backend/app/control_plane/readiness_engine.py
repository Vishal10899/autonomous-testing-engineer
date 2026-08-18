from typing import Dict, Any, List, Optional

class ReadinessEngine:
    """
    Defensible Production Readiness Engine (PRD Section 31)
    Calculates multi-domain scores: Security, Performance, Reliability, API, Database, AI Quality, Regression.
    Critical findings serve as immediate release blockers forcing NOT_READY status.
    """
    @staticmethod
    def calculate_readiness(test_results: List[Dict[str, Any]], findings: List[Dict[str, Any]]) -> Dict[str, Any]:
        total_tests = len(test_results)
        if total_tests == 0:
            return {
                "score": 0.0,
                "verdict": "INCONCLUSIVE",
                "summary": "No tests were executed.",
                "domains": {}
            }

        passed_tests = sum(1 for r in test_results if r.get("status") == "PASSED")
        failed_tests = sum(1 for r in test_results if r.get("status") in ("FAILED", "ANOMALY"))

        # Category breakdown across PRD Section 31 domains
        domains = {
            "Functional": {"passed": 0, "total": 0, "score": 100.0},
            "API": {"passed": 0, "total": 0, "score": 100.0},
            "Security": {"passed": 0, "total": 0, "score": 100.0},
            "Performance": {"passed": 0, "total": 0, "score": 100.0},
            "Reliability": {"passed": 0, "total": 0, "score": 100.0},
            "Database": {"passed": 0, "total": 0, "score": 100.0},
            "AI Quality": {"passed": 0, "total": 0, "score": 100.0},
            "Regression": {"passed": 0, "total": 0, "score": 100.0}
        }

        for r in test_results:
            cat = r.get("category", "Functional")
            if cat == "AI":
                cat = "AI Quality"
            if cat not in domains:
                cat = "Functional"
            domains[cat]["total"] += 1
            if r.get("status") == "PASSED":
                domains[cat]["passed"] += 1

        for cat in domains:
            if domains[cat]["total"] > 0:
                domains[cat]["score"] = round((domains[cat]["passed"] / domains[cat]["total"]) * 100.0, 1)

        # Count severity of findings
        critical_count = sum(1 for f in findings if f.get("severity") in ("CRITICAL", "CRITICAL") and f.get("status") in ("CONFIRMED", "POTENTIAL", "INVESTIGATING"))
        high_count = sum(1 for f in findings if f.get("severity") == "HIGH" and f.get("status") in ("CONFIRMED", "POTENTIAL", "INVESTIGATING"))
        medium_count = sum(1 for f in findings if f.get("severity") == "MEDIUM" and f.get("status") in ("CONFIRMED", "POTENTIAL", "INVESTIGATING"))

        # Overall Base Score Calculation
        raw_score = (passed_tests / total_tests) * 100.0
        
        # Deduct penalties for confirmed findings
        penalty = (critical_count * 40.0) + (high_count * 20.0) + (medium_count * 5.0)
        final_score = max(0.0, min(100.0, raw_score - penalty))

        # Defensible Verdict logic (PRD Section 31)
        if critical_count > 0:
            verdict = "NOT_READY"
            reason = f"Production release blocked by {critical_count} critical finding(s)."
        elif high_count > 1 or final_score < 70.0:
            verdict = "NOT_READY"
            reason = f"Production release blocked due to high severity findings or low readiness score ({round(final_score, 1)}%)."
        elif high_count == 1 or final_score < 90.0:
            verdict = "CONDITIONAL"
            reason = f"Release requires manual sign-off due to 1 high severity finding or warnings."
        else:
            verdict = "READY"
            reason = "System verified evidence-backed ready for production deployment."

        return {
            "score": round(final_score, 1),
            "verdict": verdict,
            "reason": reason,
            "metrics": {
                "total_tests": total_tests,
                "passed_tests": passed_tests,
                "failed_tests": failed_tests,
                "critical_findings": critical_count,
                "high_findings": high_count,
                "medium_findings": medium_count
            },
            "domains": domains
        }
