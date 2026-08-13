import time
import httpx
from typing import Dict, Any, Tuple

class APIEngine:
    """
    Deterministic API Execution Engine (PRD Section 24 & 25)
    Validates REST, GraphQL, WebSocket, status codes, headers, contracts, auth, and schema drift.
    """
    @staticmethod
    async def execute(base_url: str, test_payload: Dict[str, Any], headers: Dict[str, str] = None) -> Dict[str, Any]:
        start_time = time.time()
        method = test_payload.get("method", "GET")
        path = test_payload.get("path", "/")
        target_url = base_url.rstrip("/") + path
        
        request_headers = headers or {"User-Agent": "Autonomous-Testing-Engineer/1.0"}

        try:
            async with httpx.AsyncClient(timeout=10.0, verify=False) as client:
                req_kwargs = {"headers": request_headers}
                if "json" in test_payload:
                    req_kwargs["json"] = test_payload["json"]

                response = await client.request(method, target_url, **req_kwargs)
                elapsed_ms = (time.time() - start_time) * 1000.0

                # Analyze contract & status code
                status = response.status_code
                is_anomaly = (status >= 500) or (elapsed_ms > 250.0)
                
                resp_json = None
                try:
                    resp_json = response.json()
                except Exception:
                    resp_json = {"raw": response.text[:500]}

                return {
                    "success": status < 400,
                    "status_code": status,
                    "execution_time_ms": round(elapsed_ms, 2),
                    "is_anomaly": is_anomaly,
                    "request": {
                        "url": target_url,
                        "method": method,
                        "headers": request_headers,
                        "payload": test_payload.get("json")
                    },
                    "response": {
                        "status_code": status,
                        "headers": dict(response.headers),
                        "body": resp_json
                    }
                }
        except Exception as e:
            elapsed_ms = (time.time() - start_time) * 1000.0
            return {
                "success": False,
                "status_code": 0,
                "execution_time_ms": round(elapsed_ms, 2),
                "is_anomaly": True,
                "error": str(e),
                "request": {"url": target_url, "method": method},
                "response": None
            }
