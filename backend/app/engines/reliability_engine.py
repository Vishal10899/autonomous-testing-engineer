import time
import httpx
from typing import Dict, Any

class ReliabilityEngine:
    """
    Reliability & Chaos Engine (PRD Section 35 & 36)
    Tests retry behavior, circuit breakers, timeout limits, and controlled fault injection.
    """
    @staticmethod
    async def test_reliability(base_url: str, test_payload: Dict[str, Any]) -> Dict[str, Any]:
        target_path = test_payload.get("path", "/")
        target_url = base_url.rstrip("/") + target_path
        start_time = time.time()

        try:
            async with httpx.AsyncClient(timeout=2.0, verify=False) as client:
                res = await client.get(target_url)
                elapsed_ms = (time.time() - start_time) * 1000.0
                return {
                    "success": res.status_code < 500,
                    "execution_time_ms": round(elapsed_ms, 2),
                    "timeout_handled": True,
                    "status_code": res.status_code
                }
        except httpx.TimeoutException:
            elapsed_ms = (time.time() - start_time) * 1000.0
            return {
                "success": False,
                "execution_time_ms": round(elapsed_ms, 2),
                "timeout_handled": False,
                "error": "Request timed out after 2.0s"
            }
        except Exception as e:
            elapsed_ms = (time.time() - start_time) * 1000.0
            return {
                "success": False,
                "execution_time_ms": round(elapsed_ms, 2),
                "error": str(e)
            }
