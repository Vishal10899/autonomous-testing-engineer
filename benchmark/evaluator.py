from typing import Dict, Any, List

class BenchmarkEvaluator:
    """
    Ground Truth Automated Evaluator (PRD Section 91 & 125)
    Evaluates detected findings against known ground truth defect set.
    Calculates:
    - Precision = True Positives / (True Positives + False Positives)
    - Recall = True Positives / (True Positives + False Negatives)
    - F1 Score = 2 * (Precision * Recall) / (Precision + Recall)
    - RCA Accuracy = Correct Root Cause Explanations / True Positives
    - Reproduction Rate = Successfully Reproduced / Confirmed Defects
    """
    GROUND_TRUTH_DEFECTS = [
        {"code": "DEF_BOLA", "name": "BOLA / Authorization Bypass", "endpoint": "/api/v1/user/profile", "expected_severity": "CRITICAL"},
        {"code": "DEF_SQLI", "name": "SQL Injection", "endpoint": "/api/v1/products/search", "expected_severity": "CRITICAL"},
        {"code": "DEF_RACE", "name": "Race Condition / Missing Idempotency", "endpoint": "/api/v1/checkout", "expected_severity": "CRITICAL"},
        {"code": "DEF_PERF", "name": "Performance Degradation", "endpoint": "/api/v1/analytics/report", "expected_severity": "HIGH"},
        {"code": "DEF_AI", "name": "AI Grounding & Prompt Injection", "endpoint": "/api/v1/ai/query", "expected_severity": "HIGH"}
    ]

    @staticmethod
    def evaluate_run(detected_findings: List[Dict[str, Any]]) -> Dict[str, Any]:
        true_positives = 0
        false_positives = 0
        correct_rca_count = 0
        reproduced_count = 0

        matched_ground_truth = set()

        for finding in detected_findings:
            title = finding.get("title", "")
            endpoint = finding.get("affected_endpoint", "")
            root_cause = finding.get("root_cause", "")
            repro = finding.get("reproduction_rate", "")

            matched = False
            for gt in BenchmarkEvaluator.GROUND_TRUTH_DEFECTS:
                if gt["endpoint"] in endpoint or gt["code"].lower() in title.lower() or any(k in title.lower() for k in ["bola", "sql", "race", "performance", "ai"]):
                    if gt["code"] not in matched_ground_truth:
                        matched = True
                        matched_ground_truth.add(gt["code"])
                        true_positives += 1
                        
                        if root_cause and ("authorization" in root_cause.lower() or "sql" in root_cause.lower() or "isolation" in root_cause.lower() or "unindexed" in root_cause.lower() or "rag" in root_cause.lower()):
                            correct_rca_count += 1
                        
                        if repro and "attempts" in repro:
                            reproduced_count += 1
                        break

            if not matched:
                false_positives += 1

        total_ground_truth = len(BenchmarkEvaluator.GROUND_TRUTH_DEFECTS)
        false_negatives = total_ground_truth - true_positives

        precision = (true_positives / (true_positives + false_positives)) if (true_positives + false_positives) > 0 else 0.0
        recall = (true_positives / total_ground_truth) if total_ground_truth > 0 else 0.0
        f1 = (2 * precision * recall / (precision + recall)) if (precision + recall) > 0 else 0.0
        rca_accuracy = (correct_rca_count / true_positives) if true_positives > 0 else 0.0
        repro_rate = (reproduced_count / true_positives) if true_positives > 0 else 0.0

        return {
            "total_ground_truth": total_ground_truth,
            "defects_detected": true_positives,
            "false_positives": false_positives,
            "false_negatives": false_negatives,
            "precision": round(precision * 100, 1),
            "recall": round(recall * 100, 1),
            "f1_score": round(f1 * 100, 1),
            "rca_accuracy": round(rca_accuracy * 100, 1),
            "reproduction_rate": round(repro_rate * 100, 1)
        }
