import httpx
import time
from typing import Dict, Any, List, Optional
from app.engines.sql_injection_engine import SQLInjectionEngine
from app.engines.authorization_engine import AuthorizationEngine
from app.engines.auth_resilience_engine import AuthenticationResilienceEngine
from app.engines.api_security_engine import APISecurityEngine
from app.engines.business_logic_engine import BusinessLogicEngine
from app.engines.race_condition_engine import RaceConditionEngine

class SecurityEngine:
    """
    Unified Security & Adversarial Testing Facade (PRD Sections 11–18)
    Dispatches to dedicated specialized testing engines:
    - SQLInjectionEngine (Section 13)
    - AuthenticationResilienceEngine (Section 14)
    - AuthorizationEngine (Section 15)
    - APISecurityEngine (Section 16)
    - BusinessLogicEngine (Section 17)
    - RaceConditionEngine (Section 18)
    """

    @classmethod
    async def execute_security_probe(cls, base_url: str, test_payload: Dict[str, Any]) -> Dict[str, Any]:
        attack_type = test_payload.get("attack", "bola_authorization_bypass")
        path = test_payload.get("path", "/api/v1/user/profile")

        if attack_type in ("sql_injection", "sqli"):
            return await SQLInjectionEngine.execute(base_url, test_payload)

        elif attack_type in ("bola_authorization_bypass", "authorization", "idor", "privilege_escalation"):
            return await AuthorizationEngine.execute(base_url, test_payload)

        elif attack_type in ("auth_resilience", "rate_limiting", "tampered_token", "account_enumeration"):
            return await AuthenticationResilienceEngine.execute(base_url, test_payload)

        elif attack_type in ("api_security", "cors", "verb_tampering", "sensitive_exposure"):
            return await APISecurityEngine.execute(base_url, test_payload)

        elif attack_type in ("business_logic", "price_manipulation", "coupon_stacking"):
            return await BusinessLogicEngine.execute(base_url, test_payload)

        elif attack_type in ("race_condition", "double_spend", "concurrency_race_condition"):
            return await RaceConditionEngine.execute(base_url, test_payload)

        # Default fallback security probe
        start_time = time.time()
        vulnerability_detected = False
        target_url = base_url.rstrip("/") + (path if path.startswith("/") else "/" + path)
        details = ""

        async with httpx.AsyncClient(timeout=5.0, verify=False) as client:
            res = await client.get(target_url, headers={"Authorization": "Bearer invalid_unauthorized_token"})
            if res.status_code == 200 and not any(p in path.lower() for p in ["health", "login", "register", "catalog", "search"]):
                vulnerability_detected = True
                details = f"Authorization boundary failure on {path}: Endpoint accessible with unauthorized token."
            else:
                details = f"Security baseline passed for {path}."

        elapsed_ms = (time.time() - start_time) * 1000.0
        return {
            "vulnerability_detected": vulnerability_detected,
            "attack_type": attack_type,
            "target_url": target_url,
            "execution_time_ms": round(elapsed_ms, 2),
            "details": details
        }
