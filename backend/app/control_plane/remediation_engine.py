from typing import Dict, Any, Optional

class RemediationEngine:
    """
    Remediation Engine (PRD Section 28)
    For every confirmed vulnerability, generates developer-actionable remediation:
    Problem -> Root Cause -> Recommended Fix -> Code-level guidance -> Configuration guidance -> Verification Test
    """

    @classmethod
    def generate_remediation(cls, finding_title: str, rca_info: Dict[str, Any], endpoint: Optional[str] = None) -> Dict[str, Any]:
        ep = endpoint or "/api/endpoint"
        root_cause = rca_info.get("root_cause", "Unvalidated input or missing access controls.")
        
        if "SQL" in finding_title:
            problem = f"SQL Injection vulnerability on endpoint {ep} allows database query manipulation."
            rec_fix = "Replace raw SQL query string formatting with parameterized query bindings or ORM queries."
            code_diff = (
                "```python\n"
                "- query = f\"SELECT * FROM products WHERE name LIKE '%{user_input}%'\"\n"
                "- cursor.execute(query)\n"
                "+ query = \"SELECT * FROM products WHERE name LIKE :term\"\n"
                "+ cursor.execute(query, {\"term\": f\"%{user_input}%\"})\n"
                "```"
            )
            config_guidance = "Ensure database user account holds least-privilege permissions and database query timeouts are enforced."
            verification_test = f"pytest -k 'test_sql_injection and {ep}'"

        elif "BOLA" in finding_title or "Authorization" in finding_title:
            problem = f"Broken Object Level Authorization (BOLA/IDOR) on {ep} permits unauthorized user access to sensitive records."
            rec_fix = "Enforce ownership validation before fetching or modifying resources."
            code_diff = (
                "```python\n"
                "- record = db.query(UserProfile).filter(UserProfile.id == requested_id).first()\n"
                "+ record = db.query(UserProfile).filter(\n"
                "+     UserProfile.id == requested_id,\n"
                "+     UserProfile.owner_id == current_authenticated_user.id\n"
                "+ ).first()\n"
                "+ if not record:\n"
                "+     raise HTTPException(status_code=403, detail=\"Access denied to object\")\n"
                "```"
            )
            config_guidance = "Enable centralized Policy Enforcement Point (PEP) or ABAC/RBAC middleware for all /api/v1/user/* routes."
            verification_test = f"pytest -k 'test_bola_authorization and {ep}'"

        elif "Race" in finding_title or "Concurrency" in finding_title:
            problem = f"Race condition on transactional endpoint {ep} permits duplicate state modifications."
            rec_fix = "Implement database row-level locking (SELECT FOR UPDATE) or atomic transactions with idempotency keys."
            code_diff = (
                "```python\n"
                "- balance = account.balance\n"
                "- if balance >= amount:\n"
                "-     account.balance -= amount\n"
                "+ async with db.begin():\n"
                "+     account = await db.execute(select(Account).where(Account.id == acc_id).with_for_update())\n"
                "+     if account.balance < amount:\n"
                "+         raise HTTPException(status_code=400, detail=\"Insufficient funds\")\n"
                "+     account.balance -= amount\n"
                "```"
            )
            config_guidance = "Configure database transaction isolation level to SERIALIZABLE or REPEATABLE READ for financial endpoints."
            verification_test = f"pytest -k 'test_concurrency_race_condition and {ep}'"

        elif "AI" in finding_title or "Prompt" in finding_title or "RAG" in finding_title:
            problem = f"AI component on {ep} is susceptible to adversarial prompt injection or hallucination."
            rec_fix = "Implement multi-layer input sanitization, system prompt isolation, and post-generation grounding guardrails."
            code_diff = (
                "```python\n"
                "- response = llm.generate(f\"{system_prompt}\\nUser: {user_input}\")\n"
                "+ sanitized_input = prompt_guard.sanitize(user_input)\n"
                "+ response = llm.generate_with_guardrails(sanitized_input, context=rag_chunks)\n"
                "+ if not response.is_grounded:\n"
                "+     return {\"output\": \"I cannot verify this against provided reference data.\", \"grounded\": False}\n"
                "```"
            )
            config_guidance = "Set strict grounding thresholds (>= 0.85) and disable unverified tool execution capabilities in agent runtime."
            verification_test = f"pytest -k 'test_ai_prompt_injection and {ep}'"

        else:
            problem = f"Detected defect on {ep}: {finding_title}"
            rec_fix = "Apply defensive input validation, strict error handling, and timeout policies."
            code_diff = "```python\n# Validate input schema and reject unexpected payloads\n```"
            config_guidance = "Review service security headers, rate-limiting, and error masking policies."
            verification_test = f"pytest -k 'test_endpoint and {ep}'"

        return {
            "problem": problem,
            "root_cause": root_cause,
            "recommended_fix": rec_fix,
            "code_diff": code_diff,
            "config_guidance": config_guidance,
            "verification_test": verification_test
        }
