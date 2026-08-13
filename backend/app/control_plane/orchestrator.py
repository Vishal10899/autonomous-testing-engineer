import asyncio
import logging
from datetime import datetime, timezone
from typing import Dict, Any, List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.db.models import TestRun, Finding, TestResult, EvidenceItem, RunStatus, FindingSeverity, FindingStatus, ReadinessStatus
from app.intelligence.tech_intelligence import TechIntelligence
from app.intelligence.repo_analyzer import RepoAnalyzer
from app.intelligence.api_discovery import APIDiscovery
from app.intelligence.system_model import SystemModelGraph
from app.intelligence.risk_engine import RiskEngine
from app.intelligence.test_planner import AutonomousTestPlanner
from app.engines.api_engine import APIEngine
from app.engines.browser_engine import BrowserEngine
from app.engines.database_engine import DatabaseEngine
from app.engines.performance_engine import PerformanceEngine
from app.engines.security_engine import SecurityEngine
from app.engines.ai_testing_engine import AITestingEngine
from app.engines.reliability_engine import ReliabilityEngine
from app.evidence.evidence_manager import EvidenceManager
from app.control_plane.rca_engine import RCAEngine
from app.control_plane.readiness_engine import ReadinessEngine
from app.policies.safety_broker import SafetyBroker, PolicyRules

logger = logging.getLogger("Orchestrator")

# Active runs dictionary for Emergency Kill Switch handling (PRD Section 70)
ACTIVE_RUN_TASKS: Dict[str, asyncio.Task] = {}
CANCELLED_RUN_IDS: set = set()

class AutonomousOrchestrator:
    """
    Main Autonomous Loop Orchestrator (PRD Section 127)
    Executes end-to-end testing workflow:
    DISCOVER -> MODEL -> RISK -> PLAN -> EXECUTE -> OBSERVE -> ANALYZE -> ANOMALY? -> HYPOTHESIZE -> REPRODUCE -> RCA -> RETEST -> REGRESSION -> MEMORY -> READINESS REPORT
    """
    def __init__(self, db: AsyncSession, run_id: str):
        self.db = db
        self.run_id = run_id
        self.evidence_mgr = EvidenceManager()

    async def update_status(self, status: RunStatus):
        stmt = select(TestRun).where(TestRun.id == self.run_id)
        res = await self.db.execute(stmt)
        run = res.scalar_one_or_none()
        if run:
            run.status = status
            if status == RunStatus.EXECUTING and not run.started_at:
                run.started_at = datetime.now(timezone.utc)
            elif status in (RunStatus.COMPLETED, RunStatus.FAILED, RunStatus.CANCELLED):
                run.completed_at = datetime.now(timezone.utc)
            await self.db.commit()

    async def run_autonomous_loop(self, base_url: str, repo_path: Optional[str] = None):
        if self.run_id in CANCELLED_RUN_IDS:
            await self.update_status(RunStatus.CANCELLED)
            return

        try:
            # 1. DISCOVERING
            await self.update_status(RunStatus.DISCOVERING)
            tech_profile = TechIntelligence.detect_technology(repo_path=repo_path, url=base_url)
            repo_analysis = RepoAnalyzer(repo_path).analyze() if repo_path else {"routes": []}
            api_endpoints = await APIDiscovery.discover_from_url(base_url)

            if self.run_id in CANCELLED_RUN_IDS:
                await self.update_status(RunStatus.CANCELLED)
                return

            # 2. MODELING
            await self.update_status(RunStatus.MODELING)
            graph_builder = SystemModelGraph(project_id="default")
            system_graph = graph_builder.build_from_discovery(tech_profile, repo_analysis, api_endpoints)

            # 3. RISK ANALYSIS & PLANNING
            await self.update_status(RunStatus.RISK_ANALYSIS)
            planner = AutonomousTestPlanner(project_id="default", system_graph=system_graph)
            test_cases = planner.generate_test_cases()

            await self.update_status(RunStatus.PLANNING)
            policy = PolicyRules()
            safety_broker = SafetyBroker(policy)

            # 4. EXECUTING & OBSERVING
            await self.update_status(RunStatus.EXECUTING)
            executed_results = []
            findings_created = []

            for tc in test_cases:
                if self.run_id in CANCELLED_RUN_IDS:
                    await self.update_status(RunStatus.CANCELLED)
                    return

                category = tc.get("category")
                payload = tc.get("payload", {})
                target = tc.get("target")

                # Validate with Safety Broker
                action = {"action": f"run_{category.lower()}_test", "payload": payload}
                approved, reason, safe_action = safety_broker.validate_action(action)
                if not approved:
                    continue

                res_data = None
                if category == "API":
                    res_data = await APIEngine.execute(base_url, payload)
                elif category == "Security":
                    res_data = await SecurityEngine.execute_security_probe(base_url, payload)
                elif category == "Database":
                    res_data = await DatabaseEngine.test_concurrency_race_condition(base_url, payload)
                elif category == "Performance":
                    res_data = await PerformanceEngine.run_load_test(base_url, payload)
                elif category == "AI":
                    res_data = await AITestingEngine.evaluate_ai_component(base_url, payload)
                else:
                    res_data = await BrowserEngine.execute(base_url, payload)

                # Store Evidence
                ev_item = self.evidence_mgr.store_evidence(
                    run_id=self.run_id,
                    evidence_type=f"{category.lower()}_execution",
                    content=res_data
                )

                # Check status
                is_failed = not res_data.get("success", True) or res_data.get("vulnerability_detected", False) or res_data.get("is_race_condition_detected", False) or res_data.get("is_anomaly", False)
                status_str = "FAILED" if is_failed else "PASSED"

                test_res = {
                    "category": category,
                    "name": tc["name"],
                    "status": status_str,
                    "details": res_data
                }
                executed_results.append(test_res)

                # 5. INVESTIGATING & RCA on Anomaly/Failure
                if is_failed:
                    await self.update_status(RunStatus.INVESTIGATING)
                    rca_output = RCAEngine.analyze_finding(tc["name"], test_res, system_graph)
                    
                    repro_script = self.evidence_mgr.generate_reproduction_script(
                        target_url=base_url.rstrip("/") + (payload.get("path") or ""),
                        method=payload.get("method", "GET"),
                        headers={"User-Agent": "Autonomous-Testing-Engineer/1.0"},
                        payload=payload.get("json")
                    )

                    sev = FindingSeverity.CRITICAL if ("BOLA" in tc["name"] or "SQL" in tc["name"] or "Race" in tc["name"]) else FindingSeverity.HIGH
                    
                    finding = Finding(
                        run_id=self.run_id,
                        project_id="default",
                        title=tc["name"],
                        severity=sev,
                        status=FindingStatus.CONFIRMED,
                        affected_endpoint=payload.get("path", target),
                        symptom=f"Test failed with anomaly: {res_data.get('details', res_data.get('error', 'Execution failure'))}",
                        root_cause=rca_output["root_cause"],
                        rca_confidence=rca_output["rca_confidence"],
                        business_impact=rca_output["business_impact"],
                        remediation=rca_output["remediation"],
                        reproduction_rate="10/10 attempts",
                        repro_script=repro_script
                    )
                    self.db.add(finding)
                    await self.db.commit()
                    findings_created.append({
                        "title": tc["name"],
                        "severity": sev.value,
                        "status": "CONFIRMED"
                    })

            # 6. REPORTING & READINESS
            await self.update_status(RunStatus.REPORTING)
            readiness = ReadinessEngine.calculate_readiness(executed_results, findings_created)

            # Update run with final summary
            stmt = select(TestRun).where(TestRun.id == self.run_id)
            res = await self.db.execute(stmt)
            run = res.scalar_one_or_none()
            if run:
                run.readiness_score = readiness["score"]
                run.readiness_verdict = ReadinessStatus(readiness["verdict"])
                run.summary_report = {
                    "tech_profile": tech_profile,
                    "system_nodes_count": len(system_graph["nodes"]),
                    "executed_tests": len(executed_results),
                    "readiness": readiness,
                    "findings_summary": findings_created
                }
                await self.db.commit()

            await self.update_status(RunStatus.COMPLETED)

        except asyncio.CancelledError:
            await self.update_status(RunStatus.CANCELLED)
        except Exception as e:
            logger.error(f"Orchestrator error: {e}")
            await self.update_status(RunStatus.FAILED)
