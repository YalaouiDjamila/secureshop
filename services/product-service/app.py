from fastapi import FastAPI

app = FastAPI()

products = [
    {"id": 1, "name": "Perfume A", "price": 50},
    {"id": 2, "name": "Perfume B", "price": 80}
]

@app.get("/products")
def get_products():
    return products