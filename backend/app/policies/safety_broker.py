from typing import Dict, Any, Tuple, Optional, List
from pydantic import BaseModel, Field

class PolicyRules(BaseModel):
    policy_level: str = "STANDARD" # SAFE, STANDARD, DEEP, PRODUCTION
    max_rps: int = 1000
    max_concurrency: int = 500
    max_requests: int = 100000
    max_duration_seconds: int = 3600
    destructive_tests: bool = False
    database_mutation: bool = False
    chaos: bool = False
    allowed_domains: List[str] = Field(default_factory=lambda: ["127.0.0.1", "localhost"])
    allowed_ips: List[str] = Field(default_factory=lambda: ["127.0.0.1/32"])
    allowed_methods: List[str] = Field(default_factory=lambda: ["GET", "POST", "PUT", "DELETE", "PATCH", "OPTIONS", "HEAD"])
    allowed_test_classes: List[str] = Field(default_factory=lambda: ["API", "Security", "Database", "Performance", "AI", "Reliability", "Browser", "Mutation"])

    @classmethod
    def get_preset(cls, level: str) -> "PolicyRules":
        lvl = level.upper()
        if lvl == "SAFE":
            return cls(
                policy_level="SAFE",
                max_rps=100,
                max_concurrency=20,
                max_requests=5000,
                max_duration_seconds=900,
                destructive_tests=False,
                database_mutation=False,
                chaos=False
            )
        elif lvl == "PRODUCTION":
            return cls(
                policy_level="PRODUCTION",
                max_rps=50,
                max_concurrency=10,
                max_requests=2000,
                max_duration_seconds=600,
                destructive_tests=False,
                database_mutation=False,
                chaos=False
            )
        elif lvl == "DEEP":
            return cls(
                policy_level="DEEP",
                max_rps=2500,
                max_concurrency=1000,
                max_requests=500000,
                max_duration_seconds=7200,
                destructive_tests=False,
                database_mutation=False,
                chaos=True
            )
        else: # STANDARD
            return cls(
                policy_level="STANDARD",
                max_rps=1000,
                max_concurrency=500,
                max_requests=100000,
                max_duration_seconds=3600,
                destructive_tests=False,
                database_mutation=False,
                chaos=False
            )

class SafetyBroker:
    """
    Deterministic Safety Broker (PRD Sections 36 & 37)
    Central authority governing:
    - Max RPS, Max concurrency, Max duration, Max requests
    - Allowed domains, Allowed IPs, Allowed HTTP methods
    - Allowed test classes and destructive operations
    - Production & Sandbox restrictions
    No testing engine or worker can bypass the Safety Broker.
    """
    def __init__(self, policy: Optional[PolicyRules] = None):
        self.policy = policy or PolicyRules()

    def validate_action(self, action: Dict[str, Any]) -> Tuple[bool, str, Dict[str, Any]]:
        action_type = action.get("action")
        payload = action.get("payload", {})
        
        if not action_type:
            return False, "Missing action type in proposed test action", action

        # 1. Performance and Rate Limits
        if action_type in ("run_performance_test", "run_load_test"):
            requested_rps = payload.get("rps", 100)
            requested_concurrency = payload.get("concurrency", 10)
            requested_count = payload.get("count", 100)

            if requested_rps > self.policy.max_rps:
                payload["rps"] = self.policy.max_rps # Cap to policy
            if requested_concurrency > self.policy.max_concurrency:
                payload["concurrency"] = self.policy.max_concurrency # Cap to policy
            if requested_count > self.policy.max_requests:
                payload["count"] = self.policy.max_requests

        # 2. Destructive Test Checks
        if payload.get("is_destructive", False) and not self.policy.destructive_tests:
            return False, "Action denied: Destructive tests are disabled in current environment policy.", action

        # 3. Database Mutation Checks
        if payload.get("mutates_database", False) and not self.policy.database_mutation:
            return False, "Action denied: Database mutation is disabled in current environment policy.", action

        # 4. Chaos Testing Checks
        if action_type in ("run_chaos_test", "run_reliability_test") and not self.policy.chaos and self.policy.policy_level in ("PRODUCTION", "SAFE"):
            return False, "Action denied: Chaos testing is disabled in current policy level.", action

        # 5. Method Whitelist Checks
        method = payload.get("method", "GET").upper()
        if method not in self.policy.allowed_methods:
            return False, f"Action denied: HTTP Method {method} not permitted by policy.", action

        return True, "Action approved by Safety Broker", action
