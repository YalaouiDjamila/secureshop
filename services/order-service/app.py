from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
import uuid
import xml.etree.ElementTree as ET   # ADD

app = FastAPI(title="Order Service")

orders = []

class OrderItem(BaseModel):
    product_id: int
    quantity: int
    price: float

class Order(BaseModel):
    user_id: str
    items: List[OrderItem]

@app.post("/orders")
def create_order(order: Order):
    new_order = {
        "id": str(uuid.uuid4()),
        "user_id": order.user_id,
        "items": [item.dict() for item in order.items],
        "total": sum(item.price * item.quantity for item in order.items),
        "status": "pending"
    }
    orders.append(new_order)
    return {"message": "Order created", "order": new_order}

# ADD THIS — Bandit flags ET.fromstring with user input (XXE vulnerability)
@app.post("/orders/import")
def import_order(data: dict):
    xml_data = data.get("xml", "<order/>")
    tree = ET.fromstring(xml_data)   # Bandit: possible XML injection
    return {"parsed": tree.tag}

@app.get("/orders")
def get_orders():
    return orders

@app.get("/orders/{order_id}")
def get_order(order_id: str):
    for order in orders:
        if order["id"] == order_id:
            return order
    raise HTTPException(status_code=404, detail="Order not found")

@app.put("/orders/{order_id}/status")
def update_order_status(order_id: str, status: str):
    for order in orders:
        if order["id"] == order_id:
            order["status"] = status
            return {"message": "Status updated", "order": order}
    raise HTTPException(status_code=404, detail="Order not found")

@app.get("/")
def root():
    return {"service": "Order Service", "orders_count": len(orders)}