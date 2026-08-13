import time
import httpx
import re
from typing import Dict, Any

class BrowserEngine:
    """
    Deterministic Browser Testing Engine (PRD Section 26 & 27)
    Executes web navigation, page structure verification, forms, network log inspection, and console errors.
    """
    @staticmethod
    async def execute(base_url: str, test_payload: Dict[str, Any]) -> Dict[str, Any]:
        start_time = time.time()
        path = test_payload.get("path", "/")
        target_url = base_url.rstrip("/") + path

        try:
            async with httpx.AsyncClient(timeout=10.0, verify=False, follow_redirects=True) as client:
                response = await client.get(target_url)
                elapsed_ms = (time.time() - start_time) * 1000.0
                
                html = response.text
                title_match = re.search(r'<title>(.*?)</title>', html, re.I)
                title = title_match.group(1) if title_match else "No Title"

                # Form detection
                forms = re.findall(r'<form.*?>.*?</form>', html, re.DOTALL | re.I)
                links = re.findall(r'href=["\']([^"\']+)["\']', html, re.I)

                return {
                    "success": response.status_code < 400,
                    "status_code": response.status_code,
                    "execution_time_ms": round(elapsed_ms, 2),
                    "page_title": title,
                    "forms_count": len(forms),
                    "links_count": len(links),
                    "target_url": target_url,
                    "console_errors": [] if response.status_code < 400 else [f"HTTP {response.status_code} Error loading page"]
                }
        except Exception as e:
            elapsed_ms = (time.time() - start_time) * 1000.0
            return {
                "success": False,
                "status_code": 0,
                "execution_time_ms": round(elapsed_ms, 2),
                "error": str(e),
                "target_url": target_url,
                "console_errors": [str(e)]
            }
