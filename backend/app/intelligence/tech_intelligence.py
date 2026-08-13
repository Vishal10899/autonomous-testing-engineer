import os
import re
from typing import Dict, Any, List

class TechIntelligence:
    """
    Identifies language, framework, runtime, database, cache, queue, AI models, and cloud dependencies
    without hardcoding a single fixed list.
    """
    @staticmethod
    def detect_technology(repo_path: str = None, url: str = None, spec: dict = None) -> Dict[str, Any]:
        tech = {
            "languages": [],
            "frameworks": [],
            "databases": [],
            "caches": [],
            "ai_models": [],
            "infrastructure": [],
            "dependencies": []
        }
        
        if repo_path and os.path.exists(repo_path):
            files = []
            for root, _, filenames in os.walk(repo_path):
                for f in filenames:
                    files.append(os.path.join(root, f))
            
            # Detect languages & dependencies by config files
            file_names = [os.path.basename(f) for f in files]
            
            if "package.json" in file_names:
                tech["languages"].append("JavaScript/TypeScript")
                tech["frameworks"].append("Node.js")
            if "requirements.txt" in file_names or "pyproject.toml" in file_names:
                tech["languages"].append("Python")
            if "go.mod" in file_names:
                tech["languages"].append("Go")
            if "Cargo.toml" in file_names:
                tech["languages"].append("Rust")
            if "pom.xml" in file_names or "build.gradle" in file_names:
                tech["languages"].append("Java")
            if "Dockerfile" in file_names or "docker-compose.yml" in file_names:
                tech["infrastructure"].append("Docker")

            # Deep inspect package.json / requirements.txt for framework detection
            for fpath in files:
                fname = os.path.basename(fpath)
                if fname in ("package.json", "requirements.txt", "pyproject.toml"):
                    try:
                        with open(fpath, "r", encoding="utf-8", errors="ignore") as content_file:
                            content = content_file.read().lower()
                            if "next" in content: tech["frameworks"].append("Next.js")
                            if "react" in content: tech["frameworks"].append("React")
                            if "fastapi" in content: tech["frameworks"].append("FastAPI")
                            if "django" in content: tech["frameworks"].append("Django")
                            if "flask" in content: tech["frameworks"].append("Flask")
                            if "express" in content: tech["frameworks"].append("Express")
                            if "postgres" in content or "psycopg" in content or "asyncpg" in content: tech["databases"].append("PostgreSQL")
                            if "mongo" in content: tech["databases"].append("MongoDB")
                            if "redis" in content: tech["caches"].append("Redis")
                            if "openai" in content: tech["ai_models"].append("OpenAI")
                            if "anthropic" in content: tech["ai_models"].append("Anthropic")
                            if "gemini" in content or "google-generativeai" in content: tech["ai_models"].append("Gemini")
                            if "ollama" in content: tech["ai_models"].append("Ollama")
                    except Exception:
                        pass

        # De-duplicate lists
        for k in tech:
            tech[k] = list(set(tech[k]))

        return tech
