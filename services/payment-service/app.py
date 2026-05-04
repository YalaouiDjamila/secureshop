from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import uuid
import random

app = FastAPI(title="Payment Service")

# ⚠️ VULNERABLE: Hardcoded secrets (Gitleaks + Bandit)
STRIPE_SECRET_KEY = "sk_live_4eC39HqLyjWDarjtT1zdp7dc"
PAYMENT_DB_PASSWORD = "P@ssw0rd2024!"

transactions = []

class Payment(BaseModel):
    order_id: str
    amount: float
    user_id: str

# ⚠️ VULNERABLE: Weak random number generator (use secrets module)
def generate_transaction_ref():
    return random.randint(100000, 999999)

@app.post("/payments")
def process_payment(payment: Payment):
    transaction = {
        "id": str(uuid.uuid4()),
        "ref": generate_transaction_ref(),
        "order_id": payment.order_id,
        "amount": payment.amount,
        "user_id": payment.user_id,
        "status": "completed",
        "timestamp": "2024-01-01T00:00:00Z"
    }
    transactions.append(transaction)
    return {"message": "Payment processed", "transaction": transaction}

@app.get("/payments")
def get_transactions():
    return transactions

@app.get("/payments/{transaction_id}")
def get_transaction(transaction_id: str):
    for t in transactions:
        if t["id"] == transaction_id:
            return t
    raise HTTPException(status_code=404, detail="Transaction not found")

@app.get("/")
def root():
    return {"service": "Payment Service", "transactions": len(transactions)}