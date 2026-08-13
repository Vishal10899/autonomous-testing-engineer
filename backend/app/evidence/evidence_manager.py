import os
import json
import hashlib
from datetime import datetime, timezone
from typing import Dict, Any, List

class EvidenceManager:
    """
    Evidence Engine & Integrity Manager (PRD Section 51, 52, 54)
    Computes SHA-256 hash for every request/response, trace, log, or reproduction artifact.
    Generates minimal executable Python reproduction scripts for confirmed defects.
    """
    def __init__(self, base_storage_path: str = "./evidence_storage"):
        self.base_storage_path = base_storage_path
        os.makedirs(self.base_storage_path, exist_ok=True)

    def store_evidence(self, run_id: str, evidence_type: str, content: Dict[str, Any]) -> Dict[str, Any]:
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
            "content": content
        }

        with open(storage_path, "w", encoding="utf-8") as f:
            json.dump(evidence_item, f, indent=2)

        return evidence_item

    def generate_reproduction_script(self, target_url: str, method: str, headers: Dict[str, str], payload: Any, expected_status: int = 200) -> str:
        """
        Produces clean, standalone, executable Python script to reproduce finding (PRD Section 54).
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
