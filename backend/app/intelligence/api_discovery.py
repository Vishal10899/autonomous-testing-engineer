import httpx
from typing import Dict, Any, List, Optional

class APIDiscovery:
    """
    Discovers endpoints from live URLs, OpenAPI specs, GraphQL schemas, or static specs.
    """
    @staticmethod
    async def discover_from_url(base_url: str) -> List[Dict[str, Any]]:
        endpoints = []
        common_openapi_paths = [
            "/openapi.json",
            "/api/openapi.json",
            "/v1/openapi.json",
            "/swagger.json",
            "/docs",
            "/api-docs"
        ]

        async with httpx.AsyncClient(timeout=5.0, verify=False) as client:
            # 1. Attempt to fetch OpenAPI specification directly
            for path in common_openapi_paths:
                try:
                    target = base_url.rstrip("/") + path
                    resp = await client.get(target)
                    if resp.status_code == 200 and "application/json" in resp.headers.get("content-type", ""):
                        spec = resp.json()
                        parsed = APIDiscovery.parse_openapi_spec(spec)
                        if parsed:
                            return parsed
                except Exception:
                    continue

        return endpoints

    @staticmethod
    def parse_openapi_spec(spec: Dict[str, Any]) -> List[Dict[str, Any]]:
        endpoints = []
        paths = spec.get("paths", {})
        for path, methods in paths.items():
            for method, details in methods.items():
                if method.lower() in ("get", "post", "put", "delete", "patch", "options", "head"):
                    endpoints.append({
                        "path": path,
                        "method": method.upper(),
                        "summary": details.get("summary", ""),
                        "operation_id": details.get("operationId", ""),
                        "parameters": details.get("parameters", []),
                        "request_body": details.get("requestBody", {}),
                        "responses": details.get("responses", {}),
                        "protocol": "REST"
                    })
        return endpoints
