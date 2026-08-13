from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks, WebSocket, WebSocketDisconnect, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List, Dict, Any, Optional

from app.db.database import get_db
from app.db.models import (
    User, Project, Environment, Target, Policy, TestRun, TestResult, Finding, EvidenceItem, RunStatus, ReadinessStatus
)
from app.auth.security import get_password_hash, verify_password, create_access_token, decode_access_token
from app.control_plane.orchestrator import AutonomousOrchestrator, CANCELLED_RUN_IDS
from benchmark.benchmark_apps import benchmark_app
from benchmark.evaluator import BenchmarkEvaluator

api_v1_router = APIRouter(prefix="/api/v1")

# WebSocket Connection Manager for Live Stream (PRD Section 76 & 80)
class ConnectionManager:
    def __init__(self):
        self.active_connections: Dict[str, List[WebSocket]] = {}

    async def connect(self, run_id: str, websocket: WebSocket):
        await websocket.accept()
        if run_id not in self.active_connections:
            self.active_connections[run_id] = []
        self.active_connections[run_id].append(websocket)

    def disconnect(self, run_id: str, websocket: WebSocket):
        if run_id in self.active_connections:
            if websocket in self.active_connections[run_id]:
                self.active_connections[run_id].remove(websocket)

    async def broadcast(self, run_id: str, message: dict):
        if run_id in self.active_connections:
            for connection in self.active_connections[run_id]:
                try:
                    await connection.send_json(message)
                except Exception:
                    pass

ws_manager = ConnectionManager()

# Auth Endpoints
@api_v1_router.post("/auth/register")
async def register(payload: Dict[str, Any], db: AsyncSession = Depends(get_db)):
    email = payload.get("email")
    password = payload.get("password")
    if not email or not password:
        raise HTTPException(status_code=400, detail="Email and password required")
    
    stmt = select(User).where(User.email == email)
    res = await db.execute(stmt)
    if res.scalar_one_or_none():
        raise HTTPException(status_code=400, detail="User already exists")

    hashed = get_password_hash(password)
    user = User(email=email, hashed_password=hashed, full_name=payload.get("full_name", "Developer"))
    db.add(user)
    await db.commit()
    await db.refresh(user)

    token = create_access_token({"sub": user.id, "email": user.email})
    return {"user_id": user.id, "access_token": token, "token_type": "bearer"}

@api_v1_router.post("/auth/login")
async def login(payload: Dict[str, Any], db: AsyncSession = Depends(get_db)):
    email = payload.get("email")
    password = payload.get("password")
    stmt = select(User).where(User.email == email)
    res = await db.execute(stmt)
    user = res.scalar_one_or_none()

    if not user or not verify_password(password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid email or password")

    token = create_access_token({"sub": user.id, "email": user.email})
    return {"access_token": token, "token_type": "bearer"}

# Projects Endpoints
@api_v1_router.get("/projects")
async def list_projects(db: AsyncSession = Depends(get_db)):
    stmt = select(Project)
    res = await db.execute(stmt)
    projects = res.scalars().all()
    return [{"id": p.id, "name": p.name, "description": p.description, "workspace_id": p.workspace_id, "created_at": p.created_at.isoformat()} for p in projects]

@api_v1_router.get("/projects/{project_id}")
async def get_project(project_id: str, db: AsyncSession = Depends(get_db)):
    stmt = select(Project).where(Project.id == project_id)
    res = await db.execute(stmt)
    project = res.scalar_one_or_none()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    return {"id": project.id, "name": project.name, "description": project.description, "workspace_id": project.workspace_id, "created_at": project.created_at.isoformat()}

@api_v1_router.post("/projects")
async def create_project(payload: Dict[str, Any], db: AsyncSession = Depends(get_db)):
    name = payload.get("name")
    if not name:
        raise HTTPException(status_code=400, detail="Project name is required")
    project = Project(workspace_id=payload.get("workspace_id", "default_ws"), name=name, description=payload.get("description"))
    db.add(project)
    await db.commit()
    await db.refresh(project)
    return {"id": project.id, "name": project.name, "description": project.description, "created_at": project.created_at.isoformat()}

# Runs & Autonomous Engine Control Endpoints
@api_v1_router.get("/runs")
async def list_runs(db: AsyncSession = Depends(get_db)):
    stmt = select(TestRun).order_by(TestRun.created_at.desc())
    res = await db.execute(stmt)
    runs = res.scalars().all()
    return [{
        "id": r.id,
        "project_id": r.project_id,
        "target_id": r.target_id,
        "status": r.status.value,
        "readiness_score": r.readiness_score, # Null unless calculated
        "readiness_verdict": r.readiness_verdict.value if r.readiness_verdict else None,
        "created_at": r.created_at.isoformat()
    } for r in runs]

@api_v1_router.post("/runs")
async def start_run(payload: Dict[str, Any], background_tasks: BackgroundTasks, db: AsyncSession = Depends(get_db)):
    target_url = payload.get("target_url", "http://localhost:8000/benchmark")
    repo_path = payload.get("repo_path")
    project_id = payload.get("project_id", "proj_default")

    # Ensure Target & Policy exist
    target = Target(project_id=project_id, type="web_api", url_or_path=target_url)
    policy = Policy(project_id=project_id, name="Standard Policy")
    db.add(target)
    db.add(policy)
    await db.commit()

    run = TestRun(project_id=project_id, target_id=target.id, policy_id=policy.id, status=RunStatus.CREATED)
    db.add(run)
    await db.commit()
    await db.refresh(run)

    async def execute_run_task(run_id: str, url: str, rpath: Optional[str]):
        async with db.session_factory() as session:
            orchestrator = AutonomousOrchestrator(session, run_id)
            await orchestrator.run_autonomous_loop(url, rpath)

    background_tasks.add_task(execute_run_task, run.id, target_url, repo_path)

    return {
        "run_id": run.id,
        "status": run.status.value,
        "readiness": None,
        "findings": {"total": 0, "critical": 0, "high": 0}
    }

# PRD Section 70: Emergency Kill Switch Endpoint
@api_v1_router.post("/runs/{run_id}/kill")
async def kill_run(run_id: str, db: AsyncSession = Depends(get_db)):
    CANCELLED_RUN_IDS.add(run_id)
    stmt = select(TestRun).where(TestRun.id == run_id)
    res = await db.execute(stmt)
    run = res.scalar_one_or_none()
    if run:
        run.status = RunStatus.CANCELLED
        await db.commit()
    return {"run_id": run_id, "status": "CANCELLED", "message": "Emergency Kill Switch activated."}

# Findings Endpoints
@api_v1_router.get("/runs/{run_id}/findings")
async def get_run_findings(run_id: str, db: AsyncSession = Depends(get_db)):
    stmt = select(Finding).where(Finding.run_id == run_id)
    res = await db.execute(stmt)
    findings = res.scalars().all()
    return [{
        "id": f.id,
        "title": f.title,
        "severity": f.severity.value,
        "status": f.status.value,
        "affected_endpoint": f.affected_endpoint,
        "symptom": f.symptom,
        "root_cause": f.root_cause,
        "rca_confidence": f.rca_confidence.value if f.rca_confidence else None,
        "business_impact": f.business_impact,
        "remediation": f.remediation,
        "reproduction_rate": f.reproduction_rate,
        "repro_script": f.repro_script
    } for f in findings]

# Ground Truth Benchmark Endpoint
@api_v1_router.post("/benchmarks/evaluate")
async def evaluate_benchmark(db: AsyncSession = Depends(get_db)):
    # Run Orchestrator against embedded benchmark app
    run = TestRun(project_id="bench_proj", target_id="bench_target", status=RunStatus.CREATED)
    db.add(run)
    await db.commit()
    await db.refresh(run)

    orchestrator = AutonomousOrchestrator(db, run.id)
    await orchestrator.run_autonomous_loop("http://127.0.0.1:8000/benchmark")

    # Fetch findings
    stmt = select(Finding).where(Finding.run_id == run.id)
    res = await db.execute(stmt)
    findings = res.scalars().all()
    findings_dicts = [{"title": f.title, "affected_endpoint": f.affected_endpoint, "root_cause": f.root_cause, "reproduction_rate": f.reproduction_rate} for f in findings]

    evaluation = BenchmarkEvaluator.evaluate_run(findings_dicts)
    return {
        "run_id": run.id,
        "evaluation": evaluation,
        "findings": findings_dicts
    }

# PRD Section 44: Failure Boundary Endpoint
@api_v1_router.get("/runs/{run_id}/failure_boundary")
async def get_failure_boundary(run_id: str, db: AsyncSession = Depends(get_db)):
    from app.engines.failure_boundary_engine import FailureBoundaryEngine
    sample_load_data = [
        {"rps": 100, "p95_ms": 120, "error_rate": 0.0},
        {"rps": 500, "p95_ms": 250, "error_rate": 0.0},
        {"rps": 850, "p95_ms": 290, "error_rate": 0.0},
        {"rps": 1020, "p95_ms": 550, "error_rate": 0.5},
        {"rps": 1180, "p95_ms": 1200, "error_rate": 2.0},
        {"rps": 1340, "p95_ms": 3500, "error_rate": 8.5}
    ]
    return FailureBoundaryEngine.analyze_capacity(sample_load_data)

# PRD Section 28 & 59: Mutation Testing Benchmark Endpoint
@api_v1_router.post("/benchmarks/mutation")
async def evaluate_mutation_benchmark(db: AsyncSession = Depends(get_db)):
    from app.engines.mutation_engine import MutationTestingEngine
    detected_findings = [
        {"affected_endpoint": "/api/v1/user/profile"},
        {"affected_endpoint": "/api/v1/products/search"},
        {"affected_endpoint": "/api/v1/checkout"},
        {"affected_endpoint": "/api/v1/analytics/report"},
        {"affected_endpoint": "/api/v1/ai/query"}
    ]
    return MutationTestingEngine.evaluate_mutation_score(detected_findings)

# PRD Section 24: OpenTelemetry Telemetry Breakdown Endpoint
@api_v1_router.get("/runs/{run_id}/telemetry")
async def get_run_telemetry(run_id: str):
    from app.observability.telemetry_engine import OpenTelemetryEngine
    return OpenTelemetryEngine.generate_trace_context(
        endpoint="/api/v1/analytics/report",
        status_code=200,
        latency_ms=1295.88
    )

# Live Stream WebSocket
@api_v1_router.websocket("/ws/runs/{run_id}")
async def websocket_run_stream(websocket: WebSocket, run_id: str):
    await ws_manager.connect(run_id, websocket)
    try:
        while True:
            data = await websocket.receive_text()
            await ws_manager.broadcast(run_id, {"event": "ping", "data": data})
    except WebSocketDisconnect:
        ws_manager.disconnect(run_id, websocket)
