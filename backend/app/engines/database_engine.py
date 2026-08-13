import asyncio
import time
import httpx
from typing import Dict, Any, List

class DatabaseEngine:
    """
    Database & Concurrency Testing Engine (PRD Section 28 & 29)
    Tests race conditions, duplicate transactions, lock failures, deadlocks, and idempotency violations
    by sending parallel concurrent requests to critical endpoints.
    """
    @staticmethod
    async def test_concurrency_race_condition(base_url: str, test_payload: Dict[str, Any]) -> Dict[str, Any]:
        path = test_payload.get("path", "/checkout")
        target_url = base_url.rstrip("/") + path
        concurrent_count = test_payload.get("concurrent_requests", 10)
        method = test_payload.get("method", "POST")
        body = test_payload.get("json", {"item_id": "test_1", "amount": 100})

        start_time = time.time()
        
        async def send_single_req(client, req_id):
            headers = {"X-Request-ID": f"req_{req_id}", "Content-Type": "application/json"}
            try:
                res = await client.request(method, target_url, json=body, headers=headers)
                return {"id": req_id, "status": res.status_code, "body": res.json() if res.headers.get("content-type") == "application/json" else res.text}
            except Exception as e:
                return {"id": req_id, "status": 0, "error": str(e)}

        async with httpx.AsyncClient(timeout=10.0, verify=False) as client:
            tasks = [send_single_req(client, i) for i in range(concurrent_count)]
            results = await asyncio.gather(*tasks)

        elapsed_ms = (time.time() - start_time) * 1000.0

        # Detect race condition anomaly: if multiple requests succeeded when only 1 should succeed (e.g. duplicate payment/checkout)
        successful_requests = [r for r in results if r["status"] in (200, 201)]
        is_race_condition = len(successful_requests) > 1 and ("checkout" in path or "pay" in path or "transfer" in path)

        return {
            "success": not is_race_condition,
            "is_race_condition_detected": is_race_condition,
            "concurrent_requests": concurrent_count,
            "successful_count": len(successful_requests),
            "execution_time_ms": round(elapsed_ms, 2),
            "results_sample": results[:5]
        }
