from typing import Dict, Any, Tuple, Optional
from pydantic import BaseModel

class PolicyRules(BaseModel):
    max_rps: int = 1000
    max_concurrency: int = 500
    max_requests: int = 100000
    max_duration_seconds: int = 3600
    destructive_tests: bool = False
    database_mutation: bool = False
    chaos: bool = False

class SafetyBroker:
    """
    Deterministic Safety Broker enforcing PRD Section 2.2:
    AI -> Structured Action -> Policy Engine -> Execution Broker -> Deterministic Worker.
    AI CANNOT directly execute arbitrary actions or exceed policy boundaries.
    """
    def __init__(self, policy: PolicyRules):
        self.policy = policy

    def validate_action(self, action: Dict[str, Any]) -> Tuple[bool, str, Dict[str, Any]]:
        action_type = action.get("action")
        payload = action.get("payload", {})
        
        # Check target availability & structure
        if not action_type:
            return False, "Missing action type in proposed AI action", action

        # 1. Performance limits check
        if action_type == "run_performance_test":
            requested_rps = payload.get("rps", 100)
            requested_concurrency = payload.get("concurrency", 10)
            requested_count = payload.get("count", 100)

            if requested_rps > self.policy.max_rps:
                payload["rps"] = self.policy.max_rps # Cap to policy
            if requested_concurrency > self.policy.max_concurrency:
                payload["concurrency"] = self.policy.max_concurrency # Cap to policy
            if requested_count > self.policy.max_requests:
                payload["count"] = self.policy.max_requests

        # 2. Destructive test check
        if payload.get("is_destructive", False) and not self.policy.destructive_tests:
            return False, "Action denied: Destructive tests are disabled in current environment policy.", action

        # 3. Database mutation check
        if payload.get("mutates_database", False) and not self.policy.database_mutation:
            return False, "Action denied: Database mutation is disabled in current environment policy.", action

        # 4. Chaos testing check
        if action_type == "run_chaos_test" and not self.policy.chaos:
            return False, "Action denied: Chaos testing is disabled in current environment policy.", action

        return True, "Action approved by Policy Engine", action
