import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.db.database import init_db
from app.api.v1.router import api_v1_router
from benchmark.benchmark_apps import benchmark_app

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("AutonomousTestingEngineer")

@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Initializing Autonomous Testing Engineer Database...")
    await init_db()
    logger.info("Database initialized successfully.")
    yield
    logger.info("Shutting down Autonomous Testing Engineer Control Plane.")

app = FastAPI(
    title="Autonomous Testing Engineer — Control Plane API",
    version="5.0.0",
    description="World-Class Autonomous AI Software Testing & Production-Readiness Platform",
    lifespan=lifespan
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount API v1 router
app.include_router(api_v1_router)

# Mount embedded Ground Truth Benchmark Target App
app.mount("/benchmark", benchmark_app)

@app.get("/health")
def health_check():
    return {
        "status": "HEALTHY",
        "service": "Autonomous Testing Engineer Control Plane",
        "version": "5.0.0"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
