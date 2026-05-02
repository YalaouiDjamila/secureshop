from fastapi import FastAPI, Request    # ADD Request
from fastapi.responses import HTMLResponse  # ADD
import pickle, base64                   # ADD

app = FastAPI()

products = [
    {"id": 1, "name": "Perfume A", "price": 50},
    {"id": 2, "name": "Perfume B", "price": 80}
]

@app.get("/products")
def get_products():
    return products

# ADD THIS — DAST (ZAP) will find XSS here
@app.get("/products/search", response_class=HTMLResponse)
def search_products(name: str = ""):
    # No sanitization — ZAP flags reflected XSS
    return f"<html><body><h1>Results for: {name}</h1></body></html>"

# ADD THIS — Bandit flags pickle.loads (insecure deserialization)
@app.post("/products/load")
def load_product(data: dict):
    raw = data.get("payload", "")
    obj = pickle.loads(base64.b64decode(raw))   # Bandit: pickle security issue
    return {"result": str(obj)}

@app.get("/")
def root():
    return {"service": "Product Service"}