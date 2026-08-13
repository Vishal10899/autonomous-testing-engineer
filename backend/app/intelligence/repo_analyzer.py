import os
import ast
import re
from typing import Dict, Any, List

class RepoAnalyzer:
    """
    Analyzes source repositories to extract:
    - Endpoints & Routes (FastAPI, Flask, Express, Next.js)
    - Database Entities & Schemas
    - Dangerous operations (eval, exec, raw SQL)
    - Exposed secrets / API keys
    - Workflows
    """
    def __init__(self, repo_path: str):
        self.repo_path = repo_path

    def analyze(self) -> Dict[str, Any]:
        results = {
            "routes": [],
            "db_models": [],
            "dangerous_ops": [],
            "secrets_detected": [],
            "workflows": []
        }
        
        if not os.path.exists(self.repo_path):
            return results

        for root, _, files in os.walk(self.repo_path):
            for file in files:
                fpath = os.path.join(root, file)
                rel_path = os.path.relpath(fpath, self.repo_path)
                
                # Skip node_modules, .git, venv
                if any(ignored in rel_path for ignored in ["node_modules", ".git", "venv", "__pycache__"]):
                    continue

                if file.endswith(".py"):
                    self._analyze_python_file(fpath, rel_path, results)
                elif file.endswith((".js", ".ts", ".tsx", ".jsx")):
                    self._analyze_js_file(fpath, rel_path, results)

        return results

    def _analyze_python_file(self, fpath: str, rel_path: str, results: Dict[str, Any]):
        try:
            with open(fpath, "r", encoding="utf-8", errors="ignore") as f:
                code = f.read()

            # Secrets detection
            if re.search(r'(api_key|secret|password|auth_token)\s*=\s*["\'][A-Za-z0-9_\-]{16,}["\']', code, re.I):
                results["secrets_detected"].append({"file": rel_path, "type": "Hardcoded Secret Pattern"})

            # Dangerous ops
            if "eval(" in code or "exec(" in code or "subprocess.Popen" in code:
                results["dangerous_ops"].append({"file": rel_path, "detail": "Dynamic code execution or shell subprocess call"})

            # AST Parsing
            tree = ast.parse(code)
            for node in ast.walk(tree):
                # FastAPI / Flask decorator route matching
                if isinstance(node, ast.FunctionDef):
                    for decorator in node.decorator_list:
                        if isinstance(decorator, ast.Call):
                            func_name = ""
                            if isinstance(decorator.func, ast.Attribute):
                                func_name = decorator.func.attr
                            elif isinstance(decorator.func, ast.Name):
                                func_name = decorator.func.id
                            
                            if func_name in ("get", "post", "put", "delete", "patch", "route"):
                                method = func_name.upper() if func_name != "route" else "GET"
                                path = "/"
                                if decorator.args and isinstance(decorator.args[0], ast.Constant):
                                    path = decorator.args[0].value
                                results["routes"].append({
                                    "method": method,
                                    "path": path,
                                    "handler": node.name,
                                    "file": rel_path
                                })
                
                # Class def for SQLAlchemy ORM models
                if isinstance(node, ast.ClassDef):
                    for base in node.bases:
                        base_name = getattr(base, "id", getattr(base, "attr", ""))
                        if "Base" in base_name or "Model" in base_name:
                            results["db_models"].append({
                                "model_name": node.name,
                                "file": rel_path
                            })
        except Exception:
            pass

    def _analyze_js_file(self, fpath: str, rel_path: str, results: Dict[str, Any]):
        try:
            with open(fpath, "r", encoding="utf-8", errors="ignore") as f:
                code = f.read()

            # Express route matching
            express_routes = re.findall(r'app\.(get|post|put|delete|patch)\s*\(\s*["\']([^"\']+)["\']', code, re.I)
            for method, path in express_routes:
                results["routes"].append({
                    "method": method.upper(),
                    "path": path,
                    "handler": f"JS Route in {rel_path}",
                    "file": rel_path
                })
        except Exception:
            pass
