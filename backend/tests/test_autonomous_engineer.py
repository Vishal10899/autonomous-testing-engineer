import pytest
import asyncio
from httpx import AsyncClient, ASGITransport
from app.main import app
from app.db.database import init_db
from app.policies.safety_broker import SafetyBroker, PolicyRules
from app.intelligence.tech_intelligence import TechIntelligence
from app.intelligence.system_model import SystemModelGraph
from app.intelligence.risk_engine import RiskEngine
from app.intelligence.test_planner import AutonomousTestPlanner
from app.control_plane.readiness_engine import ReadinessEngine
from benchmark.evaluator import BenchmarkEvaluator

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
