from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
import pickle
import base64
import os

app = FastAPI()

products = [
    {"id": 1, "name": "Perfume A", "price": 50},
    {"id": 2, "name": "Perfume B", "price": 80}
]

@app.get("/products")
def get_products():
    return products

# ⚠️ VULNERABLE: XSS - unsanitized user input in HTML
@app.get("/products/search", response_class=HTMLResponse)
def search_products(name: str = ""):
    return f"<html><body><h1>Results for: {name}</h1></body></html>"

# ⚠️ VULNERABLE: Insecure deserialization (pickle)
@app.post("/products/load")
def load_product(data: dict):
    raw = data.get("payload", "")
    obj = pickle.loads(base64.b64decode(raw))
    return {"result": str(obj)}

# ⚠️ VULNERABLE: Path traversal
@app.get("/products/image")
def get_image(filename: str):
    path = f"./images/{filename}"
    return {"path": path}

# ⚠️ VULNERABLE: Command injection
@app.get("/products/export")
def export_products(format: str = "json"):
    os.system(f"echo exporting in {format}")
    return {"message": f"Exporting in {format}"}

@app.get("/")
def root():
    return {"service": "Product Service"}