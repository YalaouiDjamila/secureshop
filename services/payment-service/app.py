from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import uuid

app = FastAPI(title="Payment Service")

transactions = []

class Payment(BaseModel):
    order_id: str
    amount: float
    user_id: str

@app.post("/payments")
def process_payment(payment: Payment):
    transaction = {
        "id": str(uuid.uuid4()),
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