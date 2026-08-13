from typing import Dict, Any, List

class RetestEngine:
    """
    Retest & Regression Engine (PRD Section 59, 60, 61)
    Retests confirmed findings, compares evidence before vs after, and promotes resolved/verified findings
    into the Project Memory Regression Suite.
    """
    @staticmethod
    async def retest_finding(finding: Dict[str, Any], retest_executor_func) -> Dict[str, Any]:
        """
        Executes retest and returns verdict: FIXED, STILL_FAILING, REGRESSION, or INCONCLUSIVE
        """
        initial_status = finding.get("status")
        
        # Execute test via executor function
        retest_result = await retest_executor_func()
        
        success = retest_result.get("success", False)
        
        if success:
            verdict = "FIXED"
        else:
            verdict = "STILL_FAILING"

        return {
            "finding_id": finding.get("id"),
            "initial_status": initial_status,
            "retest_result": retest_result,
            "verdict": verdict
        }

    @staticmethod
    def promote_to_regression_suite(finding: Dict[str, Any]) -> Dict[str, Any]:
        """
        Converts confirmed finding into persistent Regression Test candidate (PRD Section 60).
        """
        return {
            "finding_id": finding.get("id"),
            "name": f"Regression Guard: {finding.get('title')}",
            "trigger_condition": f"Verify {finding.get('affected_endpoint')} resists {finding.get('symptom')}",
            "expected_result": "No vulnerability or anomaly detected.",
            "repro_script": finding.get("repro_script")
        }
