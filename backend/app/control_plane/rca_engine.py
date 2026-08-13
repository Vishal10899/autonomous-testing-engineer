from typing import Dict, Any, List

class RCAEngine:
    """
    Root Cause Analysis (RCA) & Business Impact Engine (PRD Section 55, 56, 57, 58)
    Infers root cause with confidence rating (DIRECTLY_OBSERVED, STRONGLY_INFERRED, MODERATELY_INFERRED, WEAK_HYPOTHESIS),
    estimates business impact, and formulates remediation recommendations.
    """
    @staticmethod
    def analyze_finding(symptom: str, test_result: Dict[str, Any], system_graph: Dict[str, Any]) -> Dict[str, Any]:
        category = test_result.get("category", "")
        details = test_result.get("details", {})
        
        root_cause = "Unknown anomaly observed."
        confidence = "WEAK_HYPOTHESIS"
        remediation = "Investigate application logs and traces around execution time."
        
        technical_impact = "Unexpected response or behavior."
        user_impact = "Potential service degradation or error."
        financial_impact = "Low"
        security_impact = "Low"

        combined_text = (str(symptom) + " " + str(category) + " " + str(details) + " " + str(test_result)).lower()

        # Pattern analysis
        if "bola" in combined_text or "authorization" in combined_text or "profile" in combined_text:
            root_cause = "Missing endpoint authorization check (Broken Object Level Authorization)."
            confidence = "DIRECTLY_OBSERVED"
            remediation = "Enforce user role and ownership verification middleware on resource access."
            security_impact = "CRITICAL - Unauthorized access to user data."
            user_impact = "Data breach risk for end users."

        elif "sql" in combined_text or "syntax" in combined_text or "search" in combined_text:
            root_cause = "Unsanitized dynamic database query constructing SQL from raw HTTP parameters."
            confidence = "DIRECTLY_OBSERVED"
            remediation = "Use parameterized SQL queries / ORM prepared statements."
            security_impact = "CRITICAL - Database extraction or corruption."

        elif "race" in combined_text or "concurrency" in combined_text or "idempotency" in combined_text or "checkout" in combined_text:
            root_cause = "Missing database transaction isolation / missing unique idempotency key lock on critical mutation workflow."
            confidence = "STRONGLY_INFERRED"
            remediation = "Implement Redis distributed lock (e.g. Redlock) or database row-level select_for_update locking and unique idempotency keys."
            financial_impact = "HIGH - Duplicate charges or balance inconsistencies."
            user_impact = "Duplicate transactions or state corruption."

        elif "latency" in combined_text or "p99" in combined_text or "performance" in combined_text or "analytics" in combined_text:
            root_cause = "Unindexed database query bottlenecks under concurrent load causing performance degradation."
            confidence = "STRONGLY_INFERRED"
            remediation = "Add index on query predicate columns and optimize connection pool limits."
            user_impact = "Slow response times or timeout errors."

        elif "hallucination" in combined_text or "grounding" in combined_text or "prompt" in combined_text or "ai" in combined_text:
            root_cause = "RAG context retrieval failure or insufficient LLM temperature/prompt constraint."
            confidence = "STRONGLY_INFERRED"
            remediation = "Add context similarity filtering cutoff and tighten system prompt grounding instructions."

        return {
            "root_cause": root_cause,
            "rca_confidence": confidence,
            "remediation": remediation,
            "business_impact": {
                "technical_impact": technical_impact,
                "user_impact": user_impact,
                "financial_impact": financial_impact,
                "security_impact": security_impact
            }
        }
