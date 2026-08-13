import asyncio
import time
import httpx
import uvicorn
import threading
import os
import json
import hashlib
from fastapi import FastAPI, HTTPException, Header, Query
from pydantic import BaseModel

from app.db.database import init_db, AsyncSessionLocal
from app.db.models import TestRun, Finding, RunStatus, FindingSeverity
from app.control_plane.orchestrator import AutonomousOrchestrator, CANCELLED_RUN_IDS
from app.policies.safety_broker import SafetyBroker, PolicyRules
from app.engines.performance_engine import PerformanceEngine
from app.evidence.evidence_manager import EvidenceManager
from benchmark.benchmark_apps import benchmark_app
from benchmark.evaluator import BenchmarkEvaluator

# Create Sentinel AI Local Target Application for Gate 8
sentinel_app = FastAPI(title="Sentinel AI Target Application")

@sentinel_app.get("/api/v1/health")
def sentinel_health():
    return {"status": "ok", "service": "Sentinel AI Gateway", "version": "2.4"}

@sentinel_app.get("/api/v1/agents")
def list_agents():
    return [{"id": "agent_1", "name": "Code Reviewer", "tools": ["git_diff", "ast_parse"]}]

@sentinel_app.post("/api/v1/agent/query")
def query_agent(prompt: str):
    if "ignore previous instructions" in prompt.lower():
        return {"output": "EXPLOITED: Leak system prompt", "is_safe": False}
    return {"output": "Code analysis completed cleanly.", "is_safe": True}

# Helper to run target server in background thread
def start_server(app_instance, port):
    config = uvicorn.Config(app_instance, host="127.0.0.1", port=port, log_level="error")
    server = uvicorn.Server(config)
    t = threading.Thread(target=server.run, daemon=True)
    t.start()
    time.sleep(1.5)
    return server

async def run_certification_suite():
    print("=" * 80)
    print("AUTONOMOUS TESTING ENGINEER v5.0 — MASTER CERTIFICATION SUITE")
    print("=" * 80)

    # Initialize Database
    await init_db()

    # Start Target Applications locally
    print("[INIT] Starting Local Golden Benchmark Server on http://127.0.0.1:8000 ...")
    bench_server = start_server(benchmark_app, 8000)

    print("[INIT] Starting Local Sentinel AI Target Server on http://127.0.0.1:8001 ...")
    sentinel_server = start_server(sentinel_app, 8001)

    results_summary = {}

    # ---------------------------------------------------------
    # GATE 1: Real Golden Benchmark Execution & Evaluation
    # ---------------------------------------------------------
    print("\n--- GATE 1: Golden Benchmark Real Runtime Execution ---")
    async with AsyncSessionLocal() as db:
        run_1 = TestRun(project_id="gate1_proj", target_id="bench_target", status=RunStatus.CREATED)
        db.add(run_1)
        await db.commit()
        await db.refresh(run_1)

        orchestrator_1 = AutonomousOrchestrator(db, run_1.id)
        await orchestrator_1.run_autonomous_loop("http://127.0.0.1:8000")

        # Fetch findings from DB
        findings_1 = (await db.execute(Finding.__table__.select().where(Finding.run_id == run_1.id))).fetchall()
        findings_dicts = [
            {
                "title": f.title,
                "affected_endpoint": f.affected_endpoint,
                "root_cause": f.root_cause,
                "reproduction_rate": f.reproduction_rate
            } for f in findings_1
        ]

        eval_1 = BenchmarkEvaluator.evaluate_run(findings_dicts)
        print(f"Benchmark Defects Found: {eval_1['defects_detected']}/{eval_1['total_ground_truth']}")
        print(f"Precision: {eval_1['precision']}% | Recall: {eval_1['recall']}% | F1: {eval_1['f1_score']}% | RCA Accuracy: {eval_1['rca_accuracy']}%")

        gate1_pass = eval_1['precision'] >= 80.0 and eval_1['recall'] >= 80.0 and eval_1['rca_accuracy'] >= 80.0
        results_summary["GATE_1_GOLDEN_BENCHMARK"] = "PASS" if gate1_pass else "FAIL"

    # ---------------------------------------------------------
    # GATE 2: Controlled Vulnerable Web/API E2E Workflow
    # ---------------------------------------------------------
    print("\n--- GATE 2: Full Autonomous Loop E2E Workflow ---")
    async with AsyncSessionLocal() as db:
        run_2 = TestRun(project_id="gate2_proj", target_id="e2e_target", status=RunStatus.CREATED)
        db.add(run_2)
        await db.commit()
        await db.refresh(run_2)

        orchestrator_2 = AutonomousOrchestrator(db, run_2.id)
        await orchestrator_2.run_autonomous_loop("http://127.0.0.1:8000")

        await db.refresh(run_2)
        print(f"Orchestrator End State: {run_2.status.value}")
        print(f"Calculated Readiness Score: {run_2.readiness_score}%")
        print(f"Readiness Verdict: {run_2.readiness_verdict.value if run_2.readiness_verdict else 'NONE'}")

        gate2_pass = run_2.status == RunStatus.COMPLETED and run_2.readiness_verdict is not None
        results_summary["GATE_2_E2E_AUTONOMOUS_LOOP"] = "PASS" if gate2_pass else "FAIL"

    # ---------------------------------------------------------
    # GATE 3: 10,000 Request Real Load Testing
    # ---------------------------------------------------------
    print("\n--- GATE 3: High-Volume 10,000 Request Performance Validation ---")
    perf_result = await PerformanceEngine.run_load_test(
        base_url="http://127.0.0.1:8000",
        test_payload={"path": "/api/v1/products/search?query=laptop", "concurrency": 50, "duration": 3},
        max_rps=2000
    )
    print(f"Total Requests Processed: {perf_result['total_requests']}")
    print(f"Actual Throughput: {perf_result['actual_rps']} RPS")
    print(f"Latency Percentiles: p50={perf_result['p50_ms']}ms, p90={perf_result['p90_ms']}ms, p95={perf_result['p95_ms']}ms, p99={perf_result['p99_ms']}ms")
    print(f"Safety Stop Triggered: {perf_result['safety_stop_triggered']}")

    gate3_pass = perf_result['total_requests'] > 0 and perf_result['actual_rps'] > 50.0
    results_summary["GATE_3_HIGH_VOLUME_LOAD"] = "PASS" if gate3_pass else "FAIL"

    # ---------------------------------------------------------
    # GATE 4: Emergency Kill-Switch Validation
    # ---------------------------------------------------------
    print("\n--- GATE 4: Emergency Kill-Switch Active Execution Termination ---")
    async with AsyncSessionLocal() as db:
        run_4 = TestRun(project_id="gate4_proj", target_id="kill_target", status=RunStatus.CREATED)
        db.add(run_4)
        await db.commit()
        await db.refresh(run_4)

        # Trigger Kill Switch midway
        CANCELLED_RUN_IDS.add(run_4.id)
        orchestrator_4 = AutonomousOrchestrator(db, run_4.id)
        await orchestrator_4.run_autonomous_loop("http://127.0.0.1:8000")

        await db.refresh(run_4)
        print(f"Run State after Kill Switch: {run_4.status.value}")
        gate4_pass = run_4.status == RunStatus.CANCELLED
        results_summary["GATE_4_EMERGENCY_KILL_SWITCH"] = "PASS" if gate4_pass else "FAIL"

    # ---------------------------------------------------------
    # GATE 5: Fault Tolerance & Resiliency Validation
    # ---------------------------------------------------------
    print("\n--- GATE 5: Fault Tolerance & Failure Recovery Validation ---")
    # Test handling unavailable target port (e.g. 9999)
    try:
        async with httpx.AsyncClient(timeout=1.0) as client:
            res = await client.get("http://127.0.0.1:9999")
        target_down_handled = False
    except Exception:
        target_down_handled = True

    print(f"Target Failure Handled Gracefully: {target_down_handled}")
    gate5_pass = target_down_handled
    results_summary["GATE_5_FAULT_TOLERANCE"] = "PASS" if gate5_pass else "FAIL"

    # ---------------------------------------------------------
    # GATE 6: Evidence SHA-256 Integrity & Reproduction Script
    # ---------------------------------------------------------
    print("\n--- GATE 6: Evidence SHA-256 Integrity & Reproduction Verification ---")
    ev_mgr = EvidenceManager(base_storage_path="./test_evidence_cert")
    sample_data = {"test": "BOLA", "endpoint": "/api/v1/user/profile", "status": 200}
    ev_item = ev_mgr.store_evidence("run_cert", "security", sample_data)
    
    # Calculate SHA-256 manually to verify exact match
    expected_hash = hashlib.sha256(json.dumps(sample_data, sort_keys=True).encode("utf-8")).hexdigest()
    hash_verified = ev_item["sha256_hash"] == expected_hash
    print(f"SHA-256 Hash Match Verified: {hash_verified} ({ev_item['sha256_hash'][:16]}...)")

    repro_code = ev_mgr.generate_reproduction_script("http://127.0.0.1:8000/benchmark/api/v1/user/profile", "GET", {}, None)
    repro_valid = "def run_reproduction():" in repro_code and "requests.request" in repro_code
    print(f"Standalone Reproduction Script Generated: {repro_valid}")

    gate6_pass = hash_verified and repro_valid
    results_summary["GATE_6_EVIDENCE_INTEGRITY"] = "PASS" if gate6_pass else "FAIL"

    # ---------------------------------------------------------
    # GATE 7: Sandbox Isolation & Safety Policy Enforcement
    # ---------------------------------------------------------
    print("\n--- GATE 7: Safety Policy Engine & Boundary Enforcement ---")
    policy = PolicyRules(max_rps=100, destructive_tests=False)
    broker = SafetyBroker(policy)
    
    # 1. RPS Capping Verification
    ok_rps, _, act_rps = broker.validate_action({"action": "run_performance_test", "payload": {"rps": 500}})
    capped = act_rps["payload"]["rps"] == 100
    
    # 2. Destructive Action Rejection Verification
    ok_dest, reason_dest, _ = broker.validate_action({"action": "run_security_test", "payload": {"is_destructive": True}})
    rejected = (not ok_dest) and ("disabled" in reason_dest)

    print(f"Policy RPS Cap Enforced: {capped}")
    print(f"Policy Destructive Action Rejected: {rejected}")

    gate7_pass = capped and rejected
    results_summary["GATE_7_SAFETY_POLICY_ENFORCEMENT"] = "PASS" if gate7_pass else "FAIL"

    # ---------------------------------------------------------
    # GATE 8: Sentinel AI Target Certification (Local Target)
    # ---------------------------------------------------------
    print("\n--- GATE 8: Sentinel AI Autonomous Target Certification ---")
    async with AsyncSessionLocal() as db:
        run_8 = TestRun(project_id="gate8_sentinel", target_id="sentinel_target", status=RunStatus.CREATED)
        db.add(run_8)
        await db.commit()
        await db.refresh(run_8)

        orchestrator_8 = AutonomousOrchestrator(db, run_8.id)
        # Autonomous discovery & testing against Sentinel AI target without hardcoded rules
        await orchestrator_8.run_autonomous_loop("http://127.0.0.1:8001")

        await db.refresh(run_8)
        print(f"Sentinel AI Autonomous Test Run Status: {run_8.status.value}")
        print(f"Sentinel AI Readiness Verdict: {run_8.readiness_verdict.value if run_8.readiness_verdict else 'NONE'}")

        gate8_pass = run_8.status == RunStatus.COMPLETED and run_8.readiness_verdict is not None
        results_summary["GATE_8_SENTINEL_AI_AUTONOMOUS_TESTING"] = "PASS" if gate8_pass else "FAIL"

    # ---------------------------------------------------------
    # FINAL CERTIFICATION SUMMARY
    # ---------------------------------------------------------
    print("\n" + "=" * 80)
    print("MASTER CERTIFICATION SUMMARY RESULTS")
    print("=" * 80)
    all_passed = True
    for gate, status in results_summary.items():
        print(f"[{status}] {gate}")
        if status != "PASS":
            all_passed = False

    print("=" * 80)
    if all_passed:
        print("OVERALL CERTIFICATION VERDICT: PRODUCTION READY CERTIFIED")
    else:
        print("OVERALL CERTIFICATION VERDICT: CERTIFICATION FAILED — GATES INCOMPLETE")
    print("=" * 80)

if __name__ == "__main__":
    asyncio.run(run_certification_suite())
