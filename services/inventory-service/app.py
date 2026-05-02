from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import subprocess   # ADD

app = FastAPI(title="Inventory Service")

inventory = {
    1: {"product_id": 1, "stock": 100, "reserved": 0},
    2: {"product_id": 2, "stock": 80, "reserved": 0}
}

class StockUpdate(BaseModel):
    product_id: int
    quantity: int

@app.get("/inventory")
def get_inventory():
    return list(inventory.values())

@app.get("/inventory/{product_id}")
def get_product_inventory(product_id: int):
    if product_id in inventory:
        return inventory[product_id]
    raise HTTPException(status_code=404, detail="Product not found")

# ADD THIS — Bandit flags shell=True (command injection)
@app.get("/inventory/check")
def check_item(item: str):
    result = subprocess.run(
        f"echo stock check: {item}", shell=True, capture_output=True
    )
    return {"output": result.stdout.decode()}

@app.post("/inventory/reserve")
def reserve_stock(update: StockUpdate):
    if update.product_id not in inventory:
        raise HTTPException(status_code=404, detail="Product not found")
    if inventory[update.product_id]["stock"] - inventory[update.product_id]["reserved"] >= update.quantity:
        inventory[update.product_id]["reserved"] += update.quantity
        return {"message": "Stock reserved", "inventory": inventory[update.product_id]}
    raise HTTPException(status_code=400, detail="Insufficient stock")

@app.post("/inventory/release")
def release_stock(update: StockUpdate):
    if update.product_id not in inventory:
        raise HTTPException(status_code=404, detail="Product not found")
    inventory[update.product_id]["reserved"] = max(
        0, inventory[update.product_id]["reserved"] - update.quantity
    )
    return {"message": "Stock released", "inventory": inventory[update.product_id]}

@app.get("/")
def root():
    return {"service": "Inventory Service", "products": len(inventory)}