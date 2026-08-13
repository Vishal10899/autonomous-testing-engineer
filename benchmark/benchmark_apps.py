from fastapi import FastAPI, Header, HTTPException, Query, Response, status
from pydantic import BaseModel
import asyncio
from typing import Optional

# Ground Truth Benchmark App (PRD Section 89 & 120)
benchmark_app = FastAPI(title="Ground Truth Target Application for Autonomous Testing Engineer")

# Simulated state for duplicate checkout race condition testing
checkout_ledger = {}
account_balances = {"user_1": 1000}

class CheckoutRequest(BaseModel):
    user_id: str
    item_id: str
    amount: float

# Defect 1: BOLA / Authorization Bypass
@benchmark_app.get("/api/v1/user/profile")
def get_user_profile(authorization: Optional[str] = Header(None)):
    # Vulnerability: Accepts any token without authorization verification
    return {"user_id": "victim_user_99", "email": "victim@example.com", "ssn": "999-00-1234", "balance": 50000}

# Defect 2: SQL Injection
@benchmark_app.get("/api/v1/products/search")
def search_products(query: str = Query(...)):
    # Vulnerability: Raw unsanitized query simulation
    if "'" in query or "OR" in query:
        return {"error": "sqlite3.OperationalError: near 'OR': syntax error", "leaked_tables": ["users", "credit_cards", "secrets"]}
    return {"results": [{"id": 1, "name": "Standard Laptop", "price": 999}]}

# Defect 3: Race Condition / Missing Idempotency on Checkout
@benchmark_app.post("/api/v1/checkout")
async def checkout(req: CheckoutRequest):
    # Vulnerability: Artificial delay allowing race condition on concurrent balance deduction
    curr_balance = account_balances.get(req.user_id, 0)
    await asyncio.sleep(0.05) # Delay creates race window
    if curr_balance >= req.amount:
        account_balances[req.user_id] = curr_balance - req.amount
        checkout_ledger[req.item_id] = checkout_ledger.get(req.item_id, 0) + 1
        return {"status": "SUCCESS", "remaining_balance": account_balances[req.user_id]}
    else:
        raise HTTPException(status_code=400, detail="Insufficient funds")

# Defect 4: Performance Degradation Under Load
@benchmark_app.get("/api/v1/analytics/report")
async def heavy_analytics():
    # Vulnerability: Exponential delay simulating unindexed DB query under load
    await asyncio.sleep(0.3)
    return {"status": "completed", "rows": 10000}

# Defect 5: AI RAG Hallucination & Prompt Injection
@benchmark_app.post("/api/v1/ai/query")
def ai_query(prompt: str):
    if "override" in prompt.lower() or "secret" in prompt.lower():
        return {"response": "SYSTEM OVERRIDE APPROVED: Flag{prompt_injection_success}", "grounding_score": 0.12}
    return {"response": "Our company was founded in 1750 by robots.", "grounding_score": 0.45}
