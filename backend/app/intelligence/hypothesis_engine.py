import time
from typing import Dict, Any, List, Optional

class HypothesisEngine:
    """
    Hypothesis Engine & Multi-Strategy Validation (PRD Sections 10 & 12)
    Instead of immediately declaring a vulnerability on first suspicion:
    OBSERVATION -> HYPOTHESIS -> VALIDATION PLAN -> MULTIPLE TEST STRATEGIES (A, B, C, D) -> CORRELATION -> CONFIRMED / FALSE POSITIVE
    Confidence stages: OBSERVED -> SUSPECTED -> VALIDATED -> CONFIRMED
    """

    @staticmethod
    def formulate_hypothesis(observation: Dict[str, Any]) -> Dict[str, Any]:
        title = observation.get("name", "Potential Defect")
        details = observation.get("details", {})
        category = observation.get("category", "General")

        initial_confidence = 60.0
        hypothesis_statement = f"Endpoint exhibits anomalous behavior indicating potential {category} weakness."
        validation_strategies = [
            {"strategy": "Strategy_A_Parameter_Fuzzing", "description": "Mutate input parameters with alternative syntax variants"},
            {"strategy": "Strategy_B_Differential_Error", "description": "Compare error response structures against standard baseline"},
            {"strategy": "Strategy_C_Timing_Correlation", "description": "Measure latency variance across payload complexities"},
            {"strategy": "Strategy_D_Context_Comparison", "description": "Execute cross-user authentication state comparison"}
        ]

        if "SQL" in title:
            hypothesis_statement = "User-controlled input may reach a dynamically constructed database query without parameterization."
            initial_confidence = 75.0
        elif "BOLA" in title or "Authorization" in title:
            hypothesis_statement = "Endpoint may lack object-level or user-context authorization checks."
            initial_confidence = 70.0
        elif "Race" in title or "Concurrency" in title:
            hypothesis_statement = "Endpoint may lack database row-level locking or distributed lock isolation."
            initial_confidence = 65.0
        elif "Prompt" in title or "AI" in title:
            hypothesis_statement = "AI model gateway may not sanitize adversarial system override prompts or lacks grounding guardrails."
            initial_confidence = 80.0

        return {
            "hypothesis": hypothesis_statement,
            "initial_confidence": initial_confidence,
            "stage": "SUSPECTED",
            "validation_plan": validation_strategies
        }

    @staticmethod
    def cross_validate(hypothesis: Dict[str, Any], strategy_results: List[Dict[str, Any]]) -> Dict[str, Any]:
        if not strategy_results:
            return {
                "stage": "SUSPECTED",
                "final_confidence": hypothesis.get("initial_confidence", 50.0),
                "is_confirmed": False,
                "summary": "Hypothesis recorded but no independent strategies executed."
            }

        passed_strategies = [s for s in strategy_results if s.get("confirmed", True)]
        confidence_gain = (len(passed_strategies) / max(len(strategy_results), 1)) * 30.0
        final_confidence = min(99.0, hypothesis.get("initial_confidence", 60.0) + confidence_gain)

        is_confirmed = final_confidence >= 80.0 and len(passed_strategies) >= 1
        final_stage = "CONFIRMED" if is_confirmed else ("VALIDATED" if final_confidence >= 70.0 else "SUSPECTED")

        return {
            "hypothesis": hypothesis.get("hypothesis"),
            "stage": final_stage,
            "final_confidence": round(final_confidence, 1),
            "strategies_tested": len(strategy_results),
            "strategies_confirmed": len(passed_strategies),
            "is_confirmed": is_confirmed,
            "summary": f"Cross-validation completed across {len(strategy_results)} strategies with {round(final_confidence, 1)}% confidence -> {final_stage}."
        }
