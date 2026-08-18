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
    QUEUED = "QUEUED"
    DISCOVERING = "DISCOVERING"
    MODELING = "MODELING"
    RISK_ANALYSIS = "RISK_ANALYSIS"
    PLANNING = "PLANNING"
    EXECUTING = "EXECUTING"
    OBSERVING = "OBSERVING"
    VALIDATING = "VALIDATING"
    REPRODUCING = "REPRODUCING"
    RCA = "RCA"
    REMEDIATION_PENDING = "REMEDIATION_PENDING"
    RETESTING = "RETESTING"
    REGRESSION = "REGRESSION"
    CERTIFYING = "CERTIFYING"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"
    CANCELLED = "CANCELLED"
    # Backwards compatibility aliases
    AUTHORIZED = "AUTHORIZED"
    VERIFYING = "VERIFYING"
    INVESTIGATING = "INVESTIGATING"
    REPORTING = "REPORTING"
    INCONCLUSIVE = "INCONCLUSIVE"

class FindingSeverity(str, enum.Enum):
    CRITICAL = "CRITICAL"
    HIGH = "HIGH"
    MEDIUM = "MEDIUM"
    LOW = "LOW"
    INFO = "INFO"

class FindingStatus(str, enum.Enum):
    POTENTIAL = "POTENTIAL"
    OBSERVED = "OBSERVED"
    SUSPECTED = "SUSPECTED"
    VALIDATING = "VALIDATING"
    INVESTIGATING = "INVESTIGATING"
    REPRODUCING = "REPRODUCING"
    CONFIRMED = "CONFIRMED"
    FALSE_POSITIVE = "FALSE_POSITIVE"
    ACCEPTED_RISK = "ACCEPTED_RISK"
    NOT_REPRODUCIBLE = "NOT_REPRODUCIBLE"
    MITIGATED = "MITIGATED"
    RESOLVED = "RESOLVED"
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

class PolicyLevel(str, enum.Enum):
    SAFE = "SAFE"
    STANDARD = "STANDARD"
    DEEP = "DEEP"
    PRODUCTION = "PRODUCTION"

class RetestVerdict(str, enum.Enum):
    RESOLVED = "RESOLVED"
    PARTIALLY_RESOLVED = "PARTIALLY_RESOLVED"
    STILL_VULNERABLE = "STILL_VULNERABLE"
    REGRESSION = "REGRESSION"

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
    target_owner: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    target_url: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    environment: Mapped[str] = mapped_column(String, default="DEV") # DEV, TEST, STAGING, PRODUCTION
    policy_level: Mapped[str] = mapped_column(String, default="STANDARD") # SAFE, STANDARD, DEEP, PRODUCTION
    authorization_status: Mapped[str] = mapped_column(String, default="AUTHORIZED") # AUTHORIZED, PENDING, REVOKED
    authorized_domains: Mapped[List[str]] = mapped_column(JSON, default=list)
    authorized_ip_ranges: Mapped[List[str]] = mapped_column(JSON, default=list)
    authorized_endpoints: Mapped[List[str]] = mapped_column(JSON, default=list)
    testing_window: Mapped[Optional[str]] = mapped_column(String, default="ANYTIME")
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utc_now)

class Environment(Base):
    __tablename__ = "environments"
    id: Mapped[str] = mapped_column(String, primary_key=True, default=generate_uuid)
    project_id: Mapped[str] = mapped_column(String, ForeignKey("projects.id"), nullable=False)
    name: Mapped[str] = mapped_column(String, nullable=False) # DEV, TEST, STAGING, PRODUCTION
    base_url: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    is_production: Mapped[bool] = mapped_column(Boolean, default=False)
    policy_level: Mapped[str] = mapped_column(String, default="STANDARD")
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utc_now)

class Target(Base):
    __tablename__ = "targets"
    id: Mapped[str] = mapped_column(String, primary_key=True, default=generate_uuid)
    project_id: Mapped[str] = mapped_column(String, ForeignKey("projects.id"), nullable=False)
    type: Mapped[str] = mapped_column(String, nullable=False) # web, api, repo, container, ai, ml
    url_or_path: Mapped[str] = mapped_column(String, nullable=False)
    target_owner: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    authorization_status: Mapped[str] = mapped_column(String, default="AUTHORIZED")
    authorized_domains: Mapped[List[str]] = mapped_column(JSON, default=list)
    authorized_ip_ranges: Mapped[List[str]] = mapped_column(JSON, default=list)
    authorized_endpoints: Mapped[List[str]] = mapped_column(JSON, default=list)
    testing_window: Mapped[Optional[str]] = mapped_column(String, default="ANYTIME")
    max_test_intensity: Mapped[str] = mapped_column(String, default="STANDARD")
    metadata_info: Mapped[Dict[str, Any]] = mapped_column(JSON, default=dict)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utc_now)

class Policy(Base):
    __tablename__ = "policies"
    id: Mapped[str] = mapped_column(String, primary_key=True, default=generate_uuid)
    project_id: Mapped[str] = mapped_column(String, ForeignKey("projects.id"), nullable=False)
    name: Mapped[str] = mapped_column(String, nullable=False, default="Default Safety Policy")
    policy_level: Mapped[str] = mapped_column(String, default="STANDARD") # SAFE, STANDARD, DEEP, PRODUCTION
    max_rps: Mapped[int] = mapped_column(Integer, default=1000)
    max_concurrency: Mapped[int] = mapped_column(Integer, default=500)
    max_requests: Mapped[int] = mapped_column(Integer, default=100000)
    max_duration_seconds: Mapped[int] = mapped_column(Integer, default=3600)
    destructive_tests: Mapped[bool] = mapped_column(Boolean, default=False)
    database_mutation: Mapped[bool] = mapped_column(Boolean, default=False)
    chaos: Mapped[bool] = mapped_column(Boolean, default=False)
    allowed_domains: Mapped[List[str]] = mapped_column(JSON, default=list)
    allowed_ips: Mapped[List[str]] = mapped_column(JSON, default=list)
    allowed_methods: Mapped[List[str]] = mapped_column(JSON, default=lambda: ["GET", "POST", "PUT", "DELETE", "PATCH", "OPTIONS", "HEAD"])
    allowed_test_classes: Mapped[List[str]] = mapped_column(JSON, default=lambda: ["API", "Security", "Database", "Performance", "AI", "Reliability", "Browser", "Mutation", "BusinessLogic"])
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utc_now)

class SandboxExecution(Base):
    __tablename__ = "sandbox_executions"
    id: Mapped[str] = mapped_column(String, primary_key=True, default=generate_uuid)
    project_id: Mapped[str] = mapped_column(String, ForeignKey("projects.id"), nullable=False)
    run_id: Mapped[str] = mapped_column(String, nullable=False)
    status: Mapped[str] = mapped_column(String, default="CREATED") # CREATED, CONFIGURED, DEPLOYED, HEALTHY, TESTING, COLLECTED, DESTROYED
    cpu_limit: Mapped[str] = mapped_column(String, default="2.0")
    memory_limit: Mapped[str] = mapped_column(String, default="4GB")
    disk_limit: Mapped[str] = mapped_column(String, default="10GB")
    execution_timeout_seconds: Mapped[int] = mapped_column(Integer, default=600)
    domain_allowlist: Mapped[List[str]] = mapped_column(JSON, default=list)
    ip_allowlist: Mapped[List[str]] = mapped_column(JSON, default=list)
    ephemeral_target_url: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utc_now)
    destroyed_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)

class SystemNode(Base):
    __tablename__ = "system_nodes"
    id: Mapped[str] = mapped_column(String, primary_key=True, default=generate_uuid)
    project_id: Mapped[str] = mapped_column(String, ForeignKey("projects.id"), nullable=False)
    name: Mapped[str] = mapped_column(String, nullable=False)
    type: Mapped[str] = mapped_column(String, nullable=False) # Service, Page, Endpoint, Database, Cache, External API, AI Model, Queue, Webhook
    technology: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    risk_level: Mapped[str] = mapped_column(String, default="MEDIUM")
    dependencies: Mapped[List[str]] = mapped_column(JSON, default=list)
    auth_requirement: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    data_sensitivity: Mapped[str] = mapped_column(String, default="LOW") # LOW, MEDIUM, HIGH, CRITICAL_PII
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

class TestCase(Base):
    __test__ = False
    __tablename__ = "test_cases"
    id: Mapped[str] = mapped_column(String, primary_key=True, default=generate_uuid)
    project_id: Mapped[str] = mapped_column(String, ForeignKey("projects.id"), nullable=False)
    name: Mapped[str] = mapped_column(String, nullable=False)
    category: Mapped[str] = mapped_column(String, nullable=False) # Functional, API, Security, Performance, Database, AI, Chaos, Mutation, BusinessLogic
    fingerprint: Mapped[str] = mapped_column(String, index=True, nullable=False) # Semantic deduplication hash
    payload: Mapped[Dict[str, Any]] = mapped_column(JSON, default=dict)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utc_now)

class TestRun(Base):
    __test__ = False
    __tablename__ = "test_runs"
    id: Mapped[str] = mapped_column(String, primary_key=True, default=generate_uuid)
    project_id: Mapped[str] = mapped_column(String, ForeignKey("projects.id"), nullable=False)
    target_id: Mapped[str] = mapped_column(String, ForeignKey("targets.id"), nullable=False)
    policy_id: Mapped[Optional[str]] = mapped_column(String, ForeignKey("policies.id"), nullable=True)
    status: Mapped[RunStatus] = mapped_column(SQLEnum(RunStatus), default=RunStatus.CREATED)
    readiness_score: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    readiness_verdict: Mapped[Optional[ReadinessStatus]] = mapped_column(SQLEnum(ReadinessStatus), nullable=True)
    
    # PRD v8.0 Primary KPI: Human Effort Reduction Metrics
    estimated_manual_hours: Mapped[Optional[float]] = mapped_column(Float, default=0.0)
    automated_hours: Mapped[Optional[float]] = mapped_column(Float, default=0.0)
    human_review_hours: Mapped[Optional[float]] = mapped_column(Float, default=0.0)
    effort_reduction_percentage: Mapped[Optional[float]] = mapped_column(Float, default=0.0)
    effort_metrics: Mapped[Dict[str, Any]] = mapped_column(JSON, default=dict)
    
    # PRD v8.0 Coverage & Budget
    coverage_summary: Mapped[Dict[str, Any]] = mapped_column(JSON, default=dict)
    test_budget: Mapped[Dict[str, Any]] = mapped_column(JSON, default=dict)
    onboarding_mode: Mapped[str] = mapped_column(String, default="URL") # URL, OPENAPI, REPO, DOCKER, ENVIRONMENT

    summary_report: Mapped[Optional[Dict[str, Any]]] = mapped_column(JSON, nullable=True)
    started_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    completed_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utc_now)

class TestResult(Base):
    __test__ = False
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
    type: Mapped[str] = mapped_column(String, nullable=False) # request_response, screenshot, trace, log, db_snapshot, repro_script, diff
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
    confidence_score: Mapped[float] = mapped_column(Float, default=95.0) # 0 to 100
    business_impact: Mapped[Optional[Dict[str, Any]]] = mapped_column(JSON, nullable=True)
    remediation: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    remediation_diff: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    reproduction_rate: Mapped[Optional[str]] = mapped_column(String, nullable=True) # e.g. "10/10 attempts"
    repro_script: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    retest_verdict: Mapped[Optional[str]] = mapped_column(String, nullable=True) # RESOLVED, PARTIALLY_RESOLVED, STILL_VULNERABLE, REGRESSION
    evidence_hash: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    
    # PRD v8.0 Human-in-the-Loop & Review Queue
    is_human_review_required: Mapped[bool] = mapped_column(Boolean, default=False)
    human_review_notes: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    
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
    category: Mapped[str] = mapped_column(String, nullable=False)
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
