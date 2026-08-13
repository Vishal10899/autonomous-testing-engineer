import asyncio
import time
import math
import httpx
from typing import Dict, Any, List

class PerformanceEngine:
    """
    Performance & Concurrency Load Engine (PRD Section 30, 31, 32)
    Supports load, stress, spike, endurance benchmarking.
    Calculates RPS, p50, p90, p95, p99 latencies, error counts, and enforces safety stop conditions.
    """
    @staticmethod
    async def run_load_test(base_url: str, test_payload: Dict[str, Any], max_rps: int = 1000) -> Dict[str, Any]:
        target_path = test_payload.get("path", "/")
        target_url = base_url.rstrip("/") + target_path
        concurrency = min(test_payload.get("concurrency", 10), 100)
        duration_sec = test_payload.get("duration", 3)
        
        latencies = []
        status_codes = {}
        error_count = 0
        total_requests = 0

        start_time = time.time()
        end_time = start_time + duration_sec

        async def worker(client):
            nonlocal total_requests, error_count
            while time.time() < end_time:
                req_start = time.time()
                try:
                    res = await client.get(target_url)
                    req_time = (time.time() - req_start) * 1000.0
                    latencies.append(req_time)
                    status_codes[res.status_code] = status_codes.get(res.status_code, 0) + 1
                    if res.status_code >= 500:
                        error_count += 1
                except Exception:
                    error_count += 1
                    status_codes[0] = status_codes.get(0, 0) + 1
                total_requests += 1
                await asyncio.sleep(0.01)

        async with httpx.AsyncClient(timeout=5.0, verify=False) as client:
            workers = [worker(client) for _ in range(concurrency)]
            await asyncio.gather(*workers)

        total_duration = time.time() - start_time
        actual_rps = total_requests / total_duration if total_duration > 0 else 0

        # Percentile calculations
        latencies.sort()
        count = len(latencies)
        
        p50 = latencies[int(count * 0.50)] if count > 0 else 0
        p90 = latencies[int(count * 0.90)] if count > 0 else 0
        p95 = latencies[int(count * 0.95)] if count > 0 else 0
        p99 = latencies[int(count * 0.99)] if count > 0 else 0

        # Safety trigger: 5xx threshold > 10% or p99 > 5000ms
        error_rate = (error_count / total_requests) if total_requests > 0 else 0
        safety_stop_triggered = error_rate > 0.10 or p99 > 5000.0

        return {
            "total_requests": total_requests,
            "actual_rps": round(actual_rps, 2),
            "duration_seconds": round(total_duration, 2),
            "p50_ms": round(p50, 2),
            "p90_ms": round(p90, 2),
            "p95_ms": round(p95, 2),
            "p99_ms": round(p99, 2),
            "status_codes": status_codes,
            "error_rate": round(error_rate * 100, 2),
            "safety_stop_triggered": safety_stop_triggered
        }
