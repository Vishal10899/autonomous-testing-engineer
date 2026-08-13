import hashlib
import json
from typing import Dict, Any, List
from .risk_engine import RiskEngine

class AutonomousTestPlanner:
    __test__ = False
    """
    Generates risk-based test cases across Functional, API, Security, Performance, Database, AI/LLM, Reliability domains.
    Applies SHA-256 semantic deduplication (PRD Section 23).
    """
    def __init__(self, project_id: str, system_graph: Dict[str, Any]):
        self.project_id = project_id
        self.system_graph = system_graph

    def generate_plan(self) -> Dict[str, Any]:
        return {"project_id": self.project_id, "system_graph": self.system_graph}

    def generate_test_cases(self) -> List[Dict[str, Any]]:
        test_cases = []
        seen_fingerprints = set()

        nodes = self.system_graph.get("nodes", [])
        for node in nodes:
            node_type = node.get("type", "")
            risk_info = RiskEngine.calculate_node_risk(node)
            node_name = node.get("name", "")

            # 1. API Endpoints
            if node_type == "Endpoint":
                meta = node.get("metadata_info", {})
                path = meta.get("path", node_name)
                method = meta.get("method", "GET")

                # Happy Path API Test
                tc = self._create_test_case(
                    name=f"API Contract Validation - {method} {path}",
                    category="API",
                    target=path,
                    payload={"method": method, "path": path, "type": "contract"},
                    priority=risk_info["score"]
                )
                if tc["fingerprint"] not in seen_fingerprints:
                    seen_fingerprints.add(tc["fingerprint"])
                    test_cases.append(tc)

                # Auth & Authorization BOLA Test for Sensitive Endpoints
                if risk_info["security"] >= 7.0:
                    tc_auth = self._create_test_case(
                        name=f"Security Authorization Bypass (BOLA) - {method} {path}",
                        category="Security",
                        target=path,
                        payload={"method": method, "path": path, "attack": "bola_authorization_bypass"},
                        priority=risk_info["score"] * 1.2
                    )
                    if tc_auth["fingerprint"] not in seen_fingerprints:
                        seen_fingerprints.add(tc_auth["fingerprint"])
                        test_cases.append(tc_auth)

                # SQL Injection test if receiving params or search query
                if method in ("POST", "PUT", "DELETE") or "?" in path or any(k in path.lower() for k in ["search", "query", "find", "filter"]):
                    tc_sqli = self._create_test_case(
                        name=f"Security SQL Injection Probe - {method} {path}",
                        category="Security",
                        target=path,
                        payload={"method": method, "path": path, "attack": "sql_injection"},
                        priority=risk_info["score"]
                    )
                    if tc_sqli["fingerprint"] not in seen_fingerprints:
                        seen_fingerprints.add(tc_sqli["fingerprint"])
                        test_cases.append(tc_sqli)

                # AI Grounding / Prompt Injection test for AI endpoints
                if any(k in path.lower() for k in ["ai", "prompt", "llm", "chat", "agent"]):
                    tc_ai = self._create_test_case(
                        name=f"AI Grounding, Hallucination & Prompt Injection Test - {method} {path}",
                        category="AI",
                        target=path,
                        payload={"method": method, "path": path, "test_type": "rag_grounding_prompt_injection"},
                        priority=risk_info["score"] * 1.3
                    )
                    if tc_ai["fingerprint"] not in seen_fingerprints:
                        seen_fingerprints.add(tc_ai["fingerprint"])
                        test_cases.append(tc_ai)

                # Concurrency / Race Condition Test if Financial / Transactional
                if risk_info["financial"] >= 7.0 or risk_info["concurrency"] >= 5.0 or "checkout" in path.lower():
                    tc_race = self._create_test_case(
                        name=f"Concurrency & Idempotency Duplicate Request - {method} {path}",
                        category="Database",
                        target=path,
                        payload={"method": method, "path": path, "attack": "concurrency_race_condition", "concurrent_requests": 10},
                        priority=risk_info["score"] * 1.5
                    )
                    if tc_race["fingerprint"] not in seen_fingerprints:
                        seen_fingerprints.add(tc_race["fingerprint"])
                        test_cases.append(tc_race)

            # 2. Database Nodes
            elif node_type == "Database":
                tc_db = self._create_test_case(
                    name=f"Database Deadlock & Isolation Test - {node_name}",
                    category="Database",
                    target=node_name,
                    payload={"target": node_name, "test_type": "deadlock_isolation"},
                    priority=risk_info["score"]
                )
                if tc_db["fingerprint"] not in seen_fingerprints:
                    seen_fingerprints.add(tc_db["fingerprint"])
                    test_cases.append(tc_db)

            # 3. AI / LLM Nodes
            elif node_type == "AI Model":
                tc_ai = self._create_test_case(
                    name=f"AI Grounding, Hallucination & Prompt Injection Test - {node_name}",
                    category="AI",
                    target=node_name,
                    payload={"target": node_name, "test_type": "rag_grounding_prompt_injection"},
                    priority=risk_info["score"]
                )
                if tc_ai["fingerprint"] not in seen_fingerprints:
                    seen_fingerprints.add(tc_ai["fingerprint"])
                    test_cases.append(tc_ai)

        # Always include global Performance baseline & Reliability load tests
        perf_tc = self._create_test_case(
            name="Performance Baseline & Concurrency Load Test",
            category="Performance",
            target="system_under_test",
            payload={"concurrency": 20, "rps": 100, "duration": 5},
            priority=8.0
        )
        if perf_tc["fingerprint"] not in seen_fingerprints:
            test_cases.append(perf_tc)

        # Sort by priority score descending
        test_cases.sort(key=lambda x: x["priority"], reverse=True)
        return test_cases

    def _create_test_case(self, name: str, category: str, target: str, payload: Dict[str, Any], priority: float) -> Dict[str, Any]:
        # Semantic Fingerprint Calculation (PRD Section 23)
        raw_fingerprint_str = f"{category}:{target}:{json.dumps(payload, sort_keys=True)}"
        fingerprint = hashlib.sha256(raw_fingerprint_str.encode("utf-8")).hexdigest()

        return {
            "name": name,
            "category": category,
            "target": target,
            "fingerprint": fingerprint,
            "payload": payload,
            "priority": priority
        }
