from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()

users = []

class User(BaseModel):
    username: str
    password: str

@app.post("/register")
def register(user: User):
    users.append(user)
    return {"message": "User registered"}

@app.post("/login")
def login(user: User):
    for u in users:
        if u.username == user.username and u.password == user.password:
            return {"message": "Login successful"}
    raise HTTPException(status_code=401, detail="Invalid credentials")