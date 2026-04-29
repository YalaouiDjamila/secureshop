from fastapi import FastAPI
import requests

app = FastAPI()

@app.get("/orders/{product_id}")
def create_order(product_id: int):
    product = requests.get("http://product-service:8000/products").json()

    return {
        "message": "Order created",
        "product": product
    }