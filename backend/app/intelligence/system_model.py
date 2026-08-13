from typing import Dict, Any, List, Optional
import uuid

class SystemModelGraph:
    """
    Universal System Model (PRD Section 10)
    System Graph representation mapping services, pages, endpoints, databases, caches, external APIs, and dependencies.
    """
    def __init__(self, project_id: str):
        self.project_id = project_id
        self.nodes: Dict[str, Dict[str, Any]] = {}
        self.edges: List[Dict[str, Any]] = []

    def add_node(self, node_id: str, name: str, node_type: str, technology: Optional[str] = None, risk_level: str = "MEDIUM", metadata: Dict[str, Any] = None) -> str:
        if not node_id:
            node_id = f"node_{uuid.uuid4().hex[:8]}"
        
        self.nodes[node_id] = {
            "id": node_id,
            "project_id": self.project_id,
            "name": name,
            "type": node_type,
            "technology": technology,
            "risk_level": risk_level,
            "metadata_info": metadata or {},
            "confidence": 1.0
        }
        return node_id

    def add_edge(self, source_id: str, target_id: str, relationship: str, confidence: float = 1.0, metadata: Dict[str, Any] = None):
        self.edges.append({
            "id": f"edge_{uuid.uuid4().hex[:8]}",
            "project_id": self.project_id,
            "source_node_id": source_id,
            "target_node_id": target_id,
            "relationship": relationship,
            "confidence": confidence,
            "metadata_info": metadata or {}
        })

    def build_from_discovery(self, tech_profile: Dict[str, Any], repo_analysis: Dict[str, Any], api_endpoints: List[Dict[str, Any]]):
        # 1. Main Service Node
        service_id = self.add_node(
            node_id="target_app",
            name="Target System Under Test",
            node_type="Service",
            technology=", ".join(tech_profile.get("frameworks", ["Web Service"])),
            risk_level="HIGH"
        )

        # 2. Database & Cache Nodes
        for db in tech_profile.get("databases", []):
            db_id = self.add_node(
                node_id=f"db_{db.lower()}",
                name=f"{db} Database",
                node_type="Database",
                technology=db,
                risk_level="CRITICAL"
            )
            self.add_edge(service_id, db_id, "reads_writes_to")

        for cache in tech_profile.get("caches", []):
            c_id = self.add_node(
                node_id=f"cache_{cache.lower()}",
                name=f"{cache} Cache",
                node_type="Cache",
                technology=cache,
                risk_level="MEDIUM"
            )
            self.add_edge(service_id, c_id, "caches_in")

        for ai in tech_profile.get("ai_models", []):
            ai_id = self.add_node(
                node_id=f"ai_{ai.lower()}",
                name=f"{ai} AI Model Provider",
                node_type="AI Model",
                technology=ai,
                risk_level="HIGH"
            )
            self.add_edge(service_id, ai_id, "invokes_llm")

        # 3. Endpoint Nodes
        all_routes = repo_analysis.get("routes", []) + api_endpoints
        seen_routes = set()
        for ep in all_routes:
            path = ep.get("path")
            method = ep.get("method", "GET")
            key = f"{method}_{path}"
            if key in seen_routes:
                continue
            seen_routes.add(key)
            
            # Elevated risk for critical routes
            is_critical = any(kw in path.lower() for kw in ["checkout", "pay", "auth", "login", "admin", "token", "transfer"])
            risk = "CRITICAL" if is_critical else "MEDIUM"
            
            ep_id = self.add_node(
                node_id=f"ep_{len(seen_routes)}",
                name=f"{method} {path}",
                node_type="Endpoint",
                technology="HTTP/REST",
                risk_level=risk,
                metadata={"path": path, "method": method}
            )
            self.add_edge(service_id, ep_id, "exposes_endpoint")

        return self.to_dict()

    def to_dict(self) -> Dict[str, Any]:
        return {
            "nodes": list(self.nodes.values()),
            "edges": self.edges
        }
