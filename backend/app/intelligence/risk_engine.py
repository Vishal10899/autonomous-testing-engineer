from typing import Dict, Any, List

class RiskEngine:
    """
    Computes risk score and risk multiplier according to PRD Section 16 & 17:
    Risk = (Business Impact x Security Sensitivity x Financial Impact x Mutation Rate x Concurrency x AI Involvement)
    """
    @staticmethod
    def calculate_node_risk(node: Dict[str, Any]) -> Dict[str, Any]:
        node_name = node.get("name", "").lower()
        node_type = node.get("type", "")
        tech = str(node.get("technology", "")).lower()
        
        impact_score = 5.0
        security_score = 5.0
        financial_score = 1.0
        concurrency_risk = 1.0
        ai_involvement = 1.0
        
        # Keyword heuristic analysis
        if any(w in node_name for w in ["pay", "checkout", "billing", "card", "deposit", "withdraw", "money"]):
            financial_score = 10.0
            impact_score = 9.5

        if any(w in node_name for w in ["auth", "login", "register", "token", "password", "session", "admin"]):
            security_score = 10.0
            impact_score = 9.0

        if any(w in node_name for w in ["concurrency", "race", "lock", "transaction", "transfer"]):
            concurrency_risk = 8.0

        if "ai" in node_type.lower() or "llm" in tech or "prompt" in node_name:
            ai_involvement = 7.5

        total_risk_score = (impact_score * 0.3) + (security_score * 0.3) + (financial_score * 0.2) + (concurrency_risk * 0.1) + (ai_involvement * 0.1)
        
        if total_risk_score >= 7.5:
            risk_level = "CRITICAL"
        elif total_risk_score >= 5.5:
            risk_level = "HIGH"
        elif total_risk_score >= 3.5:
            risk_level = "MEDIUM"
        else:
            risk_level = "LOW"

        return {
            "score": round(total_risk_score, 2),
            "level": risk_level,
            "impact": impact_score,
            "security": security_score,
            "financial": financial_score,
            "concurrency": concurrency_risk,
            "ai": ai_involvement
        }
