import os
import json
import hashlib
import zipfile
import io
from datetime import datetime, timezone
from typing import Dict, Any, List, Optional

class EvidenceManager:
    """
    Evidence Engine & Evidence Graph Manager (PRD Sections 25, 26, 46)
    - Computes immutable SHA-256 hash for every request/response, trace, log, or reproduction artifact.
    - Generates minimal executable Python reproduction scripts for confirmed defects.
    - Constructs relational Evidence Graphs:
      Target -> Endpoint -> Test -> Request -> Observation -> Finding -> Evidence -> RCA -> Fix -> Retest
    - Generates downloadable evidence packages.
    """
    def __init__(self, base_storage_path: str = "./evidence_storage"):
        self.base_storage_path = base_storage_path
        os.makedirs(self.base_storage_path, exist_ok=True)

    def store_evidence(self, run_id: str, evidence_type: str, content: Dict[str, Any], metadata: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        # Compute SHA-256 integrity hash
        serialized = json.dumps(content, sort_keys=True).encode("utf-8")
        sha256_hash = hashlib.sha256(serialized).hexdigest()

        evidence_filename = f"{run_id}_{evidence_type}_{sha256_hash[:10]}.json"
        storage_path = os.path.join(self.base_storage_path, evidence_filename)

        evidence_item = {
            "run_id": run_id,
            "type": evidence_type,
            "sha256_hash": sha256_hash,
            "storage_path": storage_path,
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "metadata": metadata or {},
            "content": content
        }

        with open(storage_path, "w", encoding="utf-8") as f:
            json.dump(evidence_item, f, indent=2)

        return evidence_item

    def generate_reproduction_script(self, target_url: str, method: str, headers: Dict[str, str], payload: Any, expected_status: int = 200) -> str:
        """
        Produces clean, standalone, executable Python script to reproduce finding (PRD Section 25).
        """
        script = f"""# Autonomous Testing Engineer - Automated Defect Reproduction Script
# Target: {target_url}
# Method: {method}

import requests

def run_reproduction():
    url = "{target_url}"
    headers = {json.dumps(headers or {}, indent=4)}
    payload = {json.dumps(payload, indent=4) if payload else 'None'}
    
    print(f"[REPRO] Triggering {method} {{url}}...")
    try:
        response = requests.request("{method}", url, headers=headers, json=payload, timeout=10)
        print(f"[REPRO] Received Status Code: {{response.status_code}}")
        print(f"[REPRO] Response Body: {{response.text[:300]}}")
        if response.status_code != {expected_status}:
            print("[REPRO RESULT] FAILURE REPRODUCED! Behavior deviates from expected status {expected_status}.")
            return True
        else:
            print("[REPRO RESULT] Behavior matches expected status. Defect not reproduced.")
            return False
    except Exception as e:
        print(f"[REPRO ERROR] Exception during execution: {{e}}")
        return True

if __name__ == "__main__":
    run_reproduction()
"""
        return script

    def build_evidence_graph(self, target_url: str, findings: List[Dict[str, Any]], evidence_items: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        PRD Section 26: Generates interactive relational Evidence Graph
        Target -> Endpoint -> Test -> Request -> Observation -> Finding -> Evidence -> RCA -> Fix -> Retest
        """
        nodes = []
        edges = []
        
        target_node_id = f"target_{hashlib.md5(target_url.encode()).hexdigest()[:8]}"
        nodes.append({"id": target_node_id, "label": f"Target: {target_url}", "type": "TARGET", "status": "ACTIVE"})

        for idx, finding in enumerate(findings):
            f_id = finding.get("id", f"finding_{idx}")
            endpoint = finding.get("affected_endpoint", "/api")
            ep_node_id = f"ep_{hashlib.md5(endpoint.encode()).hexdigest()[:8]}"
            test_node_id = f"test_{f_id}"
            finding_node_id = f"finding_node_{f_id}"
            rca_node_id = f"rca_{f_id}"
            fix_node_id = f"fix_{f_id}"
            retest_node_id = f"retest_{f_id}"

            # Nodes
            nodes.append({"id": ep_node_id, "label": f"Endpoint: {endpoint}", "type": "ENDPOINT"})
            nodes.append({"id": test_node_id, "label": f"Test: {finding.get('title')}", "type": "TEST"})
            nodes.append({"id": finding_node_id, "label": f"Finding: {finding.get('title')}", "type": "FINDING", "severity": finding.get("severity", "HIGH")})
            nodes.append({"id": rca_node_id, "label": f"RCA: {finding.get('root_cause', 'Unknown')[:40]}...", "type": "RCA"})
            nodes.append({"id": fix_node_id, "label": "Remediation Guidance", "type": "FIX"})
            nodes.append({"id": retest_node_id, "label": f"Retest: {finding.get('retest_verdict', 'PENDING')}", "type": "RETEST"})

            # Edges
            edges.append({"source": target_node_id, "target": ep_node_id, "relation": "exposes"})
            edges.append({"source": ep_node_id, "target": test_node_id, "relation": "targeted_by"})
            edges.append({"source": test_node_id, "target": finding_node_id, "relation": "detected"})
            edges.append({"source": finding_node_id, "target": rca_node_id, "relation": "explained_by"})
            edges.append({"source": rca_node_id, "target": fix_node_id, "relation": "remediated_by"})
            edges.append({"source": fix_node_id, "target": retest_node_id, "relation": "verified_by"})

        return {
            "target_url": target_url,
            "total_nodes": len(nodes),
            "total_edges": len(edges),
            "nodes": nodes,
            "edges": edges
        }

    def export_evidence_package(self, run_id: str, findings: List[Dict[str, Any]], evidence_items: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        PRD Section 46: Generates downloadable evidence bundle
        """
        package_manifest = {
            "run_id": run_id,
            "generated_at": datetime.now(timezone.utc).isoformat(),
            "findings_count": len(findings),
            "evidence_items_count": len(evidence_items),
            "findings": findings,
            "evidence_items": evidence_items
        }
        manifest_path = os.path.join(self.base_storage_path, f"{run_id}_evidence_manifest.json")
        with open(manifest_path, "w", encoding="utf-8") as f:
            json.dump(package_manifest, f, indent=2)

        return {
            "manifest_path": manifest_path,
            "run_id": run_id,
            "manifest": package_manifest
        }
