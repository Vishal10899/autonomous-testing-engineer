from typing import Dict, Any, List

class MutationTestingEngine:
    """
    PRD Section 28 & 59: Mutation Testing Engine
    Evaluates ATE's self-testing quality by injecting controlled mutations
    (auth bypass, SQLi, latency, boundary error) into target application nodes
    and measuring ATE's Mutation Score (Defects Detected / Total Mutations).
    """

    AVAILABLE_MUTATIONS = [
        {"id": "MUT_01", "name": "REMOVE_AUTH_CHECK", "category": "security", "target": "/api/v1/user/profile"},
        {"id": "MUT_02", "name": "INJECT_SQLI_STRING", "category": "security", "target": "/api/v1/products/search"},
        {"id": "MUT_03", "name": "REMOVE_ISOLATION_LOCK", "category": "concurrency", "target": "/api/v1/checkout"},
        {"id": "MUT_04", "name": "INJECT_DB_LATENCY_500MS", "category": "performance", "target": "/api/v1/analytics/report"},
        {"id": "MUT_05", "name": "BYPASS_RAG_GROUNDING_CHECK", "category": "ai", "target": "/api/v1/ai/query"}
    ]

    @staticmethod
    def evaluate_mutation_score(detected_findings: List[Dict[str, Any]]) -> Dict[str, Any]:
        total_mutations = len(MutationTestingEngine.AVAILABLE_MUTATIONS)
        mutations_killed = 0
        killed_details = []

        detected_endpoints = {f.get("affected_endpoint") for f in detected_findings if f.get("affected_endpoint")}

        for mut in MutationTestingEngine.AVAILABLE_MUTATIONS:
            if mut["target"] in detected_endpoints:
                mutations_killed += 1
                killed_details.append({"mutation": mut["name"], "status": "KILLED", "target": mut["target"]})
            else:
                killed_details.append({"mutation": mut["name"], "status": "SURVIVED", "target": mut["target"]})

        mutation_score = (mutations_killed / total_mutations) * 100.0 if total_mutations > 0 else 100.0

        return {
            "total_mutations": total_mutations,
            "mutations_killed": mutations_killed,
            "mutations_survived": total_mutations - mutations_killed,
            "mutation_score": round(mutation_score, 2),
            "details": killed_details
        }
