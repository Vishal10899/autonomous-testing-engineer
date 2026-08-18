import pytest
import asyncio
import socket
import threading
import time
import uvicorn
from httpx import AsyncClient, ASGITransport
from app.main import app
from app.db.database import init_db, AsyncSessionLocal
from app.db.models import TestRun, Finding, RunStatus
from app.policies.safety_broker import SafetyBroker, PolicyRules
from app.intelligence.tech_intelligence import TechIntelligence
from app.intelligence.system_model import SystemModelGraph
from app.intelligence.risk_engine import RiskEngine
from app.intelligence.test_planner import AutonomousTestPlanner
from app.control_plane.readiness_engine import ReadinessEngine
from app.control_plane.orchestrator import AutonomousOrchestrator
from benchmark.benchmark_apps import benchmark_app
from benchmark.evaluator import BenchmarkEvaluator
from sqlalchemy import select

@pytest.fixture(scope="session", autouse=True)
def live_benchmark_server():
    """Ensure benchmark app is accessible on 127.0.0.1:8000 for autonomous pipeline tests."""
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        s.connect(("127.0.0.1", 8000))
        s.close()
        yield
    except Exception:
        config = uvicorn.Config(benchmark_app, host="127.0.0.1", port=8000, log_level="error")
        server = uvicorn.Server(config)
        t = threading.Thread(target=server.run, daemon=True)
        t.start()
        time.sleep(1.2)
        yield

@pytest.mark.asyncio
async def test_health_endpoint():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.get("/health")
        assert response.status_code == 200
        assert response.json()["status"] == "HEALTHY"

@pytest.mark.asyncio
async def test_safety_broker_policy_enforcement():
    policy = PolicyRules(max_rps=100, destructive_tests=False)
    broker = SafetyBroker(policy)

    # 1. Test RPS Capping
    action_perf = {"action": "run_performance_test", "payload": {"rps": 500}}
    approved, reason, safe_action = broker.validate_action(action_perf)
    assert approved is True
    assert safe_action["payload"]["rps"] == 100 # Capped to policy limit

    # 2. Test Destructive Test Rejection
    action_dest = {"action": "run_security_test", "payload": {"is_destructive": True}}
    approved, reason, safe_action = broker.validate_action(action_dest)
    assert approved is False
    assert "Destructive tests are disabled" in reason

@pytest.mark.asyncio
async def test_readiness_engine_blocker_rule():
    # Test that critical blocker forces NOT_READY verdict regardless of mathematical score
    results = [{"category": "API", "status": "PASSED"}] * 10
    findings = [{"severity": "CRITICAL", "status": "CONFIRMED"}]

    readiness = ReadinessEngine.calculate_readiness(results, findings)
    assert readiness["verdict"] == "NOT_READY"
    assert "blocked by 1 critical finding" in readiness["reason"]

@pytest.mark.asyncio
async def test_benchmark_evaluator_metrics():
    # Test evaluation calculation against ground truth defects
    sample_findings = [
        {"title": "BOLA Authorization Bypass", "affected_endpoint": "/api/v1/user/profile", "root_cause": "Missing authorization check", "reproduction_rate": "10/10 attempts"},
        {"title": "SQL Injection", "affected_endpoint": "/api/v1/products/search", "root_cause": "Raw SQL query concatenation", "reproduction_rate": "10/10 attempts"},
        {"title": "Race Condition", "affected_endpoint": "/api/v1/checkout", "root_cause": "Missing transaction isolation lock", "reproduction_rate": "10/10 attempts"},
        {"title": "Performance Degradation", "affected_endpoint": "/api/v1/analytics/report", "root_cause": "Unindexed database query", "reproduction_rate": "10/10 attempts"}
    ]

    eval_result = BenchmarkEvaluator.evaluate_run(sample_findings)
    assert eval_result["defects_detected"] == 4
    assert eval_result["precision"] == 100.0
    assert eval_result["recall"] == 80.0 # 4 of 5
    assert eval_result["rca_accuracy"] == 100.0

@pytest.mark.asyncio
async def test_user_registration_and_duplicate_handling():
    await init_db()
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        import uuid
        unique_email = f"test_user_{uuid.uuid4().hex[:6]}@example.com"
        
        # 1. Fresh Registration -> SUCCESS (HTTP 200)
        reg_payload = {"email": unique_email, "password": "Password123!", "full_name": "Audit User"}
        res1 = await ac.post("/api/v1/auth/register", json=reg_payload)
        assert res1.status_code == 200
        body1 = res1.json()
        assert "access_token" in body1
        assert "user_id" in body1

        # 2. Duplicate Registration -> HTTP 400 "User already exists"
        res2 = await ac.post("/api/v1/auth/register", json=reg_payload)
        assert res2.status_code == 400
        assert res2.json()["detail"] == "User already exists"

        # 3. Login with Created Credentials -> HTTP 200
        res3 = await ac.post("/api/v1/auth/login", json={"email": unique_email, "password": "Password123!"})
        assert res3.status_code == 200
        assert "access_token" in res3.json()

@pytest.mark.asyncio
async def test_post_runs_and_background_execution():
    """
    Test POST /api/v1/runs triggers background task, creates independent DB session,
    executes autonomous pipeline without crash, persists findings, and allows finding retrieval.
    Also verifies GET /api/v1/runs, GET /api/v1/runs/{run_id}, and GET /api/v1/runs/{run_id}/findings.
    """
    await init_db()
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        # 1. Create a Test Run via POST /api/v1/runs
        payload = {
            "target_url": "http://127.0.0.1:8000",
            "repo_path": "benchmark",
            "project_id": "test_proj_1"
        }
        post_res = await ac.post("/api/v1/runs", json=payload)
        assert post_res.status_code == 200
        post_data = post_res.json()
        assert "run_id" in post_data
        run_id = post_data["run_id"]
        assert post_data["status"] == "CREATED"
        assert post_data["readiness"] is None
        assert "findings" in post_data

        # In ASGI transport with AsyncClient, BackgroundTasks run during request/response cycle
        # 2. Verify run status via GET /api/v1/runs/{run_id}
        run_res = await ac.get(f"/api/v1/runs/{run_id}")
        assert run_res.status_code == 200
        run_details = run_res.json()
        assert run_details["id"] == run_id
        assert run_details["project_id"] == "test_proj_1"
        assert run_details["status"] == "COMPLETED"
        assert run_details["readiness_verdict"] in ("READY", "CONDITIONAL", "NOT_READY")
        assert isinstance(run_details["readiness_score"], (int, float))
        assert run_details["started_at"] is not None
        assert run_details["completed_at"] is not None
        assert run_details["summary_report"] is not None

        # 3. Verify run in list endpoint GET /api/v1/runs
        list_res = await ac.get("/api/v1/runs")
        assert list_res.status_code == 200
        runs_list = list_res.json()
        assert any(r["id"] == run_id for r in runs_list)

        # 4. Verify findings retrieval via GET /api/v1/runs/{run_id}/findings
        findings_res = await ac.get(f"/api/v1/runs/{run_id}/findings")
        assert findings_res.status_code == 200
        findings = findings_res.json()
        assert isinstance(findings, list)
        assert len(findings) > 0

        # Validate findings attributes and RCA confidence
        for f in findings:
            assert "id" in f
            assert "title" in f
            assert "severity" in f
            assert "status" in f
            assert "root_cause" in f
            assert "rca_confidence" in f
            assert "business_impact" in f
            assert "remediation" in f
            assert "reproduction_rate" in f
            assert "repro_script" in f
            assert "def run_reproduction():" in f["repro_script"]

@pytest.mark.asyncio
async def test_kill_run_endpoint_and_mid_execution_cancellation():
    """
    Test emergency kill switch endpoint /api/v1/runs/{run_id}/kill and mid-execution cancellation.
    """
    await init_db()
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        # Create a run in DB directly to simulate pre-execution kill
        async with AsyncSessionLocal() as session:
            run = TestRun(project_id="kill_proj", target_id="kill_target", status=RunStatus.CREATED)
            session.add(run)
            await session.commit()
            await session.refresh(run)
            run_id = run.id

        # Trigger kill switch via HTTP endpoint
        kill_res = await ac.post(f"/api/v1/runs/{run_id}/kill")
        assert kill_res.status_code == 200
        assert kill_res.json()["status"] == "CANCELLED"

        # Verify status and completed_at in database
        run_res = await ac.get(f"/api/v1/runs/{run_id}")
        assert run_res.status_code == 200
        assert run_res.json()["status"] == "CANCELLED"
        assert run_res.json()["completed_at"] is not None

        # Also verify orchestrator respects CANCELLED_RUN_IDS when running
        async with AsyncSessionLocal() as session:
            run2 = TestRun(project_id="kill_proj2", target_id="kill_target", status=RunStatus.CREATED)
            session.add(run2)
            await session.commit()
            await session.refresh(run2)
            run2_id = run2.id

            from app.control_plane.orchestrator import CANCELLED_RUN_IDS
            CANCELLED_RUN_IDS.add(run2_id)
            orchestrator = AutonomousOrchestrator(session, run2_id)
            await orchestrator.run_autonomous_loop("http://127.0.0.1:8000")

            stmt = select(TestRun).where(TestRun.id == run2_id)
            res = await session.execute(stmt)
            cancelled_run = res.scalar_one_or_none()
            assert cancelled_run is not None
            assert cancelled_run.status == RunStatus.CANCELLED
            assert cancelled_run.completed_at is not None

@pytest.mark.asyncio
async def test_background_task_failure_marks_run_failed():
    """
    Test that when an exception occurs in the background pipeline, the run is marked FAILED
    with completed_at persisted and never left stuck in CREATED.
    """
    await init_db()
    from app.api.v1.router import execute_run_task
    import unittest.mock as mock

    async with AsyncSessionLocal() as session:
        run = TestRun(project_id="fail_test_proj", target_id="dummy_target", status=RunStatus.CREATED)
        session.add(run)
        await session.commit()
        await session.refresh(run)
        run_id = run.id

    # Simulate runtime exception inside background execute_run_task
    with mock.patch("app.intelligence.tech_intelligence.TechIntelligence.detect_technology", side_effect=RuntimeError("Simulated pipeline crash")):
        await execute_run_task(run_id, "http://invalid-url")

    # Verify the run status is updated to FAILED in the database with completed_at set
    async with AsyncSessionLocal() as session:
        stmt = select(TestRun).where(TestRun.id == run_id)
        res = await session.execute(stmt)
        updated_run = res.scalar_one_or_none()
        assert updated_run is not None
        assert updated_run.status == RunStatus.FAILED
        assert updated_run.completed_at is not None

@pytest.mark.asyncio
async def test_independent_session_lifecycle_in_background_task():
    """
    Verify that execute_run_task uses an independent AsyncSessionLocal session
    and does not depend on request-scoped session.
    """
    await init_db()
    from app.api.v1.router import execute_run_task

    async with AsyncSessionLocal() as session:
        run = TestRun(project_id="session_test_proj", target_id="session_target", status=RunStatus.CREATED)
        session.add(run)
        await session.commit()
        await session.refresh(run)
        run_id = run.id

    # Execute background task directly
    await execute_run_task(run_id, "http://127.0.0.1:8000", "benchmark")

    # Verify final database state
    async with AsyncSessionLocal() as session:
        stmt = select(TestRun).where(TestRun.id == run_id)
        res = await session.execute(stmt)
        finished_run = res.scalar_one_or_none()
        assert finished_run is not None
        assert finished_run.status == RunStatus.COMPLETED
        assert finished_run.readiness_score is not None
        assert finished_run.readiness_verdict is not None
        assert finished_run.started_at is not None
        assert finished_run.completed_at is not None
