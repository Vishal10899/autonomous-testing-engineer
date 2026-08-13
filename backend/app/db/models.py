import uuid
from datetime import datetime, timezone
from typing import Optional, Dict, Any, List
from sqlalchemy import (
    String, Text, Boolean, Integer, Float, DateTime, ForeignKey, JSON, Enum as SQLEnum
)
from sqlalchemy.orm import Mapped, mapped_column, relationship
import enum
from .database import Base

def generate_uuid() -> str:
    return str(uuid.uuid4())

def utc_now() -> datetime:
    return datetime.now(timezone.utc)

# Enums
class RunStatus(str, enum.Enum):
    CREATED = "CREATED"
    AUTHORIZED = "AUTHORIZED"
    DISCOVERING = "DISCOVERING"
    MODELING = "MODELING"
    RISK_ANALYSIS = "RISK_ANALYSIS"
    PLANNING = "PLANNING"
    QUEUED = "QUEUED"
    EXECUTING = "EXECUTING"
    OBSERVING = "OBSERVING"
    VERIFYING = "VERIFYING"
    INVESTIGATING = "INVESTIGATING"
    REPORTING = "REPORTING"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"
    CANCELLED = "CANCELLED"
    INCONCLUSIVE = "INCONCLUSIVE"

class FindingSeverity(str, enum.Enum):
    CRITICAL = "CRITICAL"
    HIGH = "HIGH"
    MEDIUM = "MEDIUM"
    LOW = "LOW"
    INFO = "INFO"

class FindingStatus(str, enum.Enum):
    POTENTIAL = "POTENTIAL"
    INVESTIGATING = "INVESTIGATING"
    REPRODUCING = "REPRODUCING"
    CONFIRMED = "CONFIRMED"
    FALSE_POSITIVE = "FALSE_POSITIVE"
    FLAKY = "FLAKY"
    ENVIRONMENT_FAILURE = "ENVIRONMENT_FAILURE"
    DEPENDENCY_FAILURE = "DEPENDENCY_FAILURE"
    INCONCLUSIVE = "INCONCLUSIVE"

class ReadinessStatus(str, enum.Enum):
    READY = "READY"
    CONDITIONAL = "CONDITIONAL"
    NOT_READY = "NOT_READY"
    INCONCLUSIVE = "INCONCLUSIVE"

class RCAConfidence(str, enum.Enum):
    DIRECTLY_OBSERVED = "DIRECTLY_OBSERVED"
    STRONGLY_INFERRED = "STRONGLY_INFERRED"
    MODERATELY_INFERRED = "MODERATELY_INFERRED"
    WEAK_HYPOTHESIS = "WEAK_HYPOTHESIS"
    UNKNOWN = "UNKNOWN"

# Core Models
class Organization(Base):
    __tablename__ = "organizations"
    id: Mapped[str] = mapped_column(String, primary_key=True, default=generate_uuid)
    name: Mapped[str] = mapped_column(String, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utc_now)

class Workspace(Base):
    __tablename__ = "workspaces"
    id: Mapped[str] = mapped_column(String, primary_key=True, default=generate_uuid)
    org_id: Mapped[str] = mapped_column(String, ForeignKey("organizations.id"), nullable=False)
    name: Mapped[str] = mapped_column(String, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utc_now)

class User(Base):
    __tablename__ = "users"
    id: Mapped[str] = mapped_column(String, primary_key=True, default=generate_uuid)
    email: Mapped[str] = mapped_column(String, unique=True, index=True, nullable=False)
    hashed_password: Mapped[str] = mapped_column(String, nullable=False)
    full_name: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    role: Mapped[str] = mapped_column(String, default="developer")
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utc_now)

class WorkspaceMember(Base):
    __tablename__ = "workspace_members"
    id: Mapped[str] = mapped_column(String, primary_key=True, default=generate_uuid)
    workspace_id: Mapped[str] = mapped_column(String, ForeignKey("workspaces.id"), nullable=False)
    user_id: Mapped[str] = mapped_column(String, ForeignKey("users.id"), nullable=False)
    role: Mapped[str] = mapped_column(String, default="member")

class Project(Base):
    __tablename__ = "projects"
    id: Mapped[str] = mapped_column(String, primary_key=True, default=generate_uuid)
    workspace_id: Mapped[str] = mapped_column(String, ForeignKey("workspaces.id"), nullable=False)
    name: Mapped[str] = mapped_column(String, nullable=False)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utc_now)

class Environment(Base):
    __tablename__ = "environments"
    id: Mapped[str] = mapped_column(String, primary_key=True, default=generate_uuid)
    project_id: Mapped[str] = mapped_column(String, ForeignKey("projects.id"), nullable=False)
    name: Mapped[str] = mapped_column(String, nullable=False) # e.g. dev, staging, prod
    base_url: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    is_production: Mapped[bool] = mapped_column(Boolean, default=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utc_now)

class Target(Base):
    __tablename__ = "targets"
    id: Mapped[str] = mapped_column(String, primary_key=True, default=generate_uuid)
    project_id: Mapped[str] = mapped_column(String, ForeignKey("projects.id"), nullable=False)
    type: Mapped[str] = mapped_column(String, nullable=False) # web, api, repo, container, ai, ml
    url_or_path: Mapped[str] = mapped_column(String, nullable=False)
    metadata_info: Mapped[Dict[str, Any]] = mapped_column(JSON, default=dict)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utc_now)

class Policy(Base):
    __tablename__ = "policies"
    id: Mapped[str] = mapped_column(String, primary_key=True, default=generate_uuid)
    project_id: Mapped[str] = mapped_column(String, ForeignKey("projects.id"), nullable=False)
    name: Mapped[str] = mapped_column(String, nullable=False, default="Default Safety Policy")
    max_rps: Mapped[int] = mapped_column(Integer, default=1000)
    max_concurrency: Mapped[int] = mapped_column(Integer, default=500)
    max_requests: Mapped[int] = mapped_column(Integer, default=100000)
    max_duration_seconds: Mapped[int] = mapped_column(Integer, default=3600)
    destructive_tests: Mapped[bool] = mapped_column(Boolean, default=False)
    database_mutation: Mapped[bool] = mapped_column(Boolean, default=False)
    chaos: Mapped[bool] = mapped_column(Boolean, default=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utc_now)

class SystemNode(Base):
    __tablename__ = "system_nodes"
    id: Mapped[str] = mapped_column(String, primary_key=True, default=generate_uuid)
    project_id: Mapped[str] = mapped_column(String, ForeignKey("projects.id"), nullable=False)
    name: Mapped[str] = mapped_column(String, nullable=False)
    type: Mapped[str] = mapped_column(String, nullable=False) # Service, Page, Endpoint, Database, Cache, External API, AI Model
    technology: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    risk_level: Mapped[str] = mapped_column(String, default="MEDIUM")
    metadata_info: Mapped[Dict[str, Any]] = mapped_column(JSON, default=dict)
    confidence: Mapped[float] = mapped_column(Float, default=1.0)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utc_now)

class SystemEdge(Base):
    __tablename__ = "system_edges"
    id: Mapped[str] = mapped_column(String, primary_key=True, default=generate_uuid)
    project_id: Mapped[str] = mapped_column(String, ForeignKey("projects.id"), nullable=False)
    source_node_id: Mapped[str] = mapped_column(String, ForeignKey("system_nodes.id"), nullable=False)
    target_node_id: Mapped[str] = mapped_column(String, ForeignKey("system_nodes.id"), nullable=False)
    relationship: Mapped[str] = mapped_column(String, nullable=False) # calls, reads, writes, depends_on
    confidence: Mapped[float] = mapped_column(Float, default=1.0)
    metadata_info: Mapped[Dict[str, Any]] = mapped_column(JSON, default=dict)

class Requirement(Base):
    __tablename__ = "requirements"
    id: Mapped[str] = mapped_column(String, primary_key=True, default=generate_uuid)
    project_id: Mapped[str] = mapped_column(String, ForeignKey("projects.id"), nullable=False)
    title: Mapped[str] = mapped_column(String, nullable=False)
    expected_behavior: Mapped[str] = mapped_column(Text, nullable=False)
    source: Mapped[str] = mapped_column(String, default="README") # README, OpenAPI, Code, Ticket

class Workflow(Base):
    __tablename__ = "workflows"
    id: Mapped[str] = mapped_column(String, primary_key=True, default=generate_uuid)
    project_id: Mapped[str] = mapped_column(String, ForeignKey("projects.id"), nullable=False)
    name: Mapped[str] = mapped_column(String, nullable=False)
    steps: Mapped[List[Dict[str, Any]]] = mapped_column(JSON, default=list)
    risk_level: Mapped[str] = mapped_column(String, default="HIGH")

class Endpoint(Base):
    __tablename__ = "endpoints"
    id: Mapped[str] = mapped_column(String, primary_key=True, default=generate_uuid)
    project_id: Mapped[str] = mapped_column(String, ForeignKey("projects.id"), nullable=False)
    path: Mapped[str] = mapped_column(String, nullable=False)
    method: Mapped[str] = mapped_column(String, nullable=False)
    protocol: Mapped[str] = mapped_column(String, default="REST")
    schema_info: Mapped[Dict[str, Any]] = mapped_column(JSON, default=dict)

class TestStrategy(Base):
    __tablename__ = "test_strategies"
    id: Mapped[str] = mapped_column(String, primary_key=True, default=generate_uuid)
    project_id: Mapped[str] = mapped_column(String, ForeignKey("projects.id"), nullable=False)
    rationale: Mapped[str] = mapped_column(Text, nullable=False)
    priorities: Mapped[List[Dict[str, Any]]] = mapped_column(JSON, default=list)

class TestCase(Base):
    __tablename__ = "test_cases"
    id: Mapped[str] = mapped_column(String, primary_key=True, default=generate_uuid)
    project_id: Mapped[str] = mapped_column(String, ForeignKey("projects.id"), nullable=False)
    name: Mapped[str] = mapped_column(String, nullable=False)
    category: Mapped[str] = mapped_column(String, nullable=False) # Functional, API, Security, Performance, Database, AI, Chaos
    fingerprint: Mapped[str] = mapped_column(String, index=True, nullable=False) # Semantic deduplication hash
    payload: Mapped[Dict[str, Any]] = mapped_column(JSON, default=dict)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utc_now)

class TestRun(Base):
    __tablename__ = "test_runs"
    id: Mapped[str] = mapped_column(String, primary_key=True, default=generate_uuid)
    project_id: Mapped[str] = mapped_column(String, ForeignKey("projects.id"), nullable=False)
    target_id: Mapped[str] = mapped_column(String, ForeignKey("targets.id"), nullable=False)
    policy_id: Mapped[Optional[str]] = mapped_column(String, ForeignKey("policies.id"), nullable=True)
    status: Mapped[RunStatus] = mapped_column(SQLEnum(RunStatus), default=RunStatus.CREATED)
    readiness_score: Mapped[Optional[float]] = mapped_column(Float, nullable=True) # Null unless calculated
    readiness_verdict: Mapped[Optional[ReadinessStatus]] = mapped_column(SQLEnum(ReadinessStatus), nullable=True)
    summary_report: Mapped[Optional[Dict[str, Any]]] = mapped_column(JSON, nullable=True)
    started_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    completed_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utc_now)

class TestResult(Base):
    __tablename__ = "test_results"
    id: Mapped[str] = mapped_column(String, primary_key=True, default=generate_uuid)
    run_id: Mapped[str] = mapped_column(String, ForeignKey("test_runs.id"), nullable=False)
    test_case_id: Mapped[str] = mapped_column(String, ForeignKey("test_cases.id"), nullable=False)
    status: Mapped[str] = mapped_column(String, nullable=False) # PASSED, FAILED, ANOMALY, SKIPPED, INCONCLUSIVE
    execution_time_ms: Mapped[float] = mapped_column(Float, default=0.0)
    details: Mapped[Dict[str, Any]] = mapped_column(JSON, default=dict)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utc_now)

class EvidenceItem(Base):
    __tablename__ = "evidence_items"
    id: Mapped[str] = mapped_column(String, primary_key=True, default=generate_uuid)
    run_id: Mapped[str] = mapped_column(String, ForeignKey("test_runs.id"), nullable=False)
    type: Mapped[str] = mapped_column(String, nullable=False) # request_response, screenshot, trace, log, db_snapshot, repro_script
    sha256_hash: Mapped[str] = mapped_column(String, nullable=False)
    storage_path: Mapped[str] = mapped_column(String, nullable=False)
    content: Mapped[Optional[Dict[str, Any]]] = mapped_column(JSON, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utc_now)

class Finding(Base):
    __tablename__ = "findings"
    id: Mapped[str] = mapped_column(String, primary_key=True, default=generate_uuid)
    run_id: Mapped[str] = mapped_column(String, ForeignKey("test_runs.id"), nullable=False)
    project_id: Mapped[str] = mapped_column(String, ForeignKey("projects.id"), nullable=False)
    title: Mapped[str] = mapped_column(String, nullable=False)
    severity: Mapped[FindingSeverity] = mapped_column(SQLEnum(FindingSeverity), default=FindingSeverity.MEDIUM)
    status: Mapped[FindingStatus] = mapped_column(SQLEnum(FindingStatus), default=FindingStatus.POTENTIAL)
    affected_endpoint: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    symptom: Mapped[str] = mapped_column(Text, nullable=False)
    root_cause: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    rca_confidence: Mapped[Optional[RCAConfidence]] = mapped_column(SQLEnum(RCAConfidence), nullable=True)
    business_impact: Mapped[Optional[Dict[str, Any]]] = mapped_column(JSON, nullable=True)
    remediation: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    reproduction_rate: Mapped[Optional[str]] = mapped_column(String, nullable=True) # e.g. "31/31 attempts"
    repro_script: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utc_now)

class FindingEvidence(Base):
    __tablename__ = "finding_evidence"
    id: Mapped[str] = mapped_column(String, primary_key=True, default=generate_uuid)
    finding_id: Mapped[str] = mapped_column(String, ForeignKey("findings.id"), nullable=False)
    evidence_id: Mapped[str] = mapped_column(String, ForeignKey("evidence_items.id"), nullable=False)

class RegressionSuite(Base):
    __tablename__ = "regression_suites"
    id: Mapped[str] = mapped_column(String, primary_key=True, default=generate_uuid)
    project_id: Mapped[str] = mapped_column(String, ForeignKey("projects.id"), nullable=False)
    name: Mapped[str] = mapped_column(String, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utc_now)

class RegressionTest(Base):
    __tablename__ = "regression_tests"
    id: Mapped[str] = mapped_column(String, primary_key=True, default=generate_uuid)
    suite_id: Mapped[str] = mapped_column(String, ForeignKey("regression_suites.id"), nullable=False)
    finding_id: Mapped[str] = mapped_column(String, ForeignKey("findings.id"), nullable=False)
    trigger_condition: Mapped[str] = mapped_column(Text, nullable=False)
    repro_steps: Mapped[Dict[str, Any]] = mapped_column(JSON, default=dict)
    expected_result: Mapped[str] = mapped_column(Text, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utc_now)

class BenchmarkApp(Base):
    __tablename__ = "benchmark_apps"
    id: Mapped[str] = mapped_column(String, primary_key=True, default=generate_uuid)
    name: Mapped[str] = mapped_column(String, nullable=False)
    category: Mapped[str] = mapped_column(String, nullable=False) # e.g. Auth, SQLi, BOLA, RaceCondition, LLM_Hallucination, etc.
    description: Mapped[str] = mapped_column(Text, nullable=False)

class BenchmarkDefect(Base):
    __tablename__ = "benchmark_defects"
    id: Mapped[str] = mapped_column(String, primary_key=True, default=generate_uuid)
    app_id: Mapped[str] = mapped_column(String, ForeignKey("benchmark_apps.id"), nullable=False)
    defect_code: Mapped[str] = mapped_column(String, nullable=False)
    title: Mapped[str] = mapped_column(String, nullable=False)
    severity: Mapped[FindingSeverity] = mapped_column(SQLEnum(FindingSeverity), nullable=False)
    ground_truth_rca: Mapped[str] = mapped_column(Text, nullable=False)
    is_hidden: Mapped[bool] = mapped_column(Boolean, default=False)

class BenchmarkRun(Base):
    __tablename__ = "benchmark_runs"
    id: Mapped[str] = mapped_column(String, primary_key=True, default=generate_uuid)
    run_id: Mapped[str] = mapped_column(String, ForeignKey("test_runs.id"), nullable=False)
    precision: Mapped[float] = mapped_column(Float, default=0.0)
    recall: Mapped[float] = mapped_column(Float, default=0.0)
    f1_score: Mapped[float] = mapped_column(Float, default=0.0)
    rca_accuracy: Mapped[float] = mapped_column(Float, default=0.0)
    defects_found: Mapped[int] = mapped_column(Integer, default=0)
    total_defects: Mapped[int] = mapped_column(Integer, default=0)
    false_positives: Mapped[int] = mapped_column(Integer, default=0)
    details: Mapped[Dict[str, Any]] = mapped_column(JSON, default=dict)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utc_now)

class AuditLog(Base):
    __tablename__ = "audit_logs"
    id: Mapped[str] = mapped_column(String, primary_key=True, default=generate_uuid)
    user_id: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    action: Mapped[str] = mapped_column(String, nullable=False)
    resource: Mapped[str] = mapped_column(String, nullable=False)
    details: Mapped[Dict[str, Any]] = mapped_column(JSON, default=dict)
    timestamp: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utc_now)
