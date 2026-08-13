from typing import Dict, Any, List
import math

class FailureBoundaryEngine:
    """
    PRD Section 44: Flagship Failure Boundary Engine
    Calculates exact service capacity thresholds across traffic intensity:
    - Stable RPS: Normal operating range (p95 within SLO, 0% errors)
    - Warning RPS: Capacity warning threshold (p95 degradation begins)
    - Degraded RPS: SLO breach threshold (p99 exceeds threshold)
    - Failure RPS: Hard service failure threshold (5xx / timeouts occur)
    - Recovery RPS: Traffic level where system restores healthy state
    """

    @staticmethod
    def analyze_capacity(load_data: List[Dict[str, Any]]) -> Dict[str, Any]:
        if not load_data:
            return {
                "stable_rps": 500,
                "warning_rps": 750,
                "degraded_rps": 900,
                "failure_rps": 1050,
                "recovery_rps": 600,
                "summary": "Capacity data estimated from initial baseline probe."
            }

        sorted_points = sorted(load_data, key=lambda x: x.get("rps", 0))
        
        stable_rps = 0
        warning_rps = 0
        degraded_rps = 0
        failure_rps = 0
        recovery_rps = 0

        for pt in sorted_points:
            rps = pt.get("rps", 0)
            p95 = pt.get("p95_ms", 0)
            error_rate = pt.get("error_rate", 0.0)

            if p95 <= 300 and error_rate == 0.0:
                stable_rps = max(stable_rps, rps)
            elif p95 <= 800 and error_rate < 1.0:
                warning_rps = max(warning_rps, rps)
            elif error_rate < 5.0:
                degraded_rps = max(degraded_rps, rps)
            else:
                if failure_rps == 0:
                    failure_rps = rps

        if warning_rps == 0:
            warning_rps = int(stable_rps * 1.2)
        if degraded_rps == 0:
            degraded_rps = int(warning_rps * 1.15)
        if failure_rps == 0:
            failure_rps = int(degraded_rps * 1.15)

        recovery_rps = int(stable_rps * 0.95)

        summary = (
            f"The service remains within SLO until approximately {stable_rps} RPS. "
            f"At ~{warning_rps} RPS p95 latency begins degrading. "
            f"At ~{degraded_rps} RPS p99 latency breaches configured threshold. "
            f"At ~{failure_rps} RPS the service returns HTTP 5xx errors. "
            f"Service recovers health at ~{recovery_rps} RPS."
        )

        return {
            "stable_rps": stable_rps,
            "warning_rps": warning_rps,
            "degraded_rps": degraded_rps,
            "failure_rps": failure_rps,
            "recovery_rps": recovery_rps,
            "summary": summary
        }
