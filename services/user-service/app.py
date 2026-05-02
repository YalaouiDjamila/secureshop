from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
import uuid
import os

# ⚠️ VULNÉRABLE: Debug mode enabled
app = FastAPI(title="User Service", debug=True)

# ⚠️ VULNÉRABLE: Hardcoded secrets (for testing)

# ⚠️ VULNÉRABLE: Hardcoded secrets
JWT_SECRET = "super-secret-key-for-testing-12345"
DATABASE_URL = "postgresql://admin:MyP@ssw0rd123!@localhost:5432/mydb"
AWS_KEY = "AKIAIOSFODNN7EXAMPLE"
SECRET_KEY = "sk-1234567890abcdefghijklmnopqrstuv"
users_db = []

class UserRegister(BaseModel):
    username: str
    password: str
    email: str = None

class UserLogin(BaseModel):
    username: str
    password: str

class UserResponse(BaseModel):
    id: str
    username: str
    email: str = None

@app.post("/register")
def register(user: UserRegister):
    for u in users_db:
        if u["username"] == user.username:
            raise HTTPException(status_code=400, detail="Username already exists")
    
    new_user = {
        "id": str(uuid.uuid4()),
        "username": user.username,
        "password": user.password,  # ⚠️ VULNÉRABLE: Plain text
        "email": user.email
    }
    users_db.append(new_user)
    return {"message": "User registered successfully", "user_id": new_user["id"]}

@app.post("/login")
def login(user: UserLogin):
    for u in users_db:
        if u["username"] == user.username and u["password"] == user.password:
            return {
                "message": "Login successful",
                "user_id": u["id"],
                "username": u["username"]
            }
    raise HTTPException(status_code=401, detail="Invalid credentials")

@app.get("/users")
def get_users():
    return [
        {"id": u["id"], "username": u["username"], "email": u.get("email")}
        for u in users_db
    ]

@app.get("/users/{user_id}")
def get_user(user_id: str):
    for u in users_db:
        if u["id"] == user_id:
            return {"id": u["id"], "username": u["username"], "email": u.get("email")}
    raise HTTPException(status_code=404, detail="User not found")

# ⚠️ VULNÉRABLE: Command injection
@app.get("/users/export")
def export_users(format: str = "json"):
    os.system(f"echo 'Exporting users in {format} format'")
    return {"message": f"Exporting in {format}"}

# ⚠️ VULNÉRABLE: SQL injection pattern
@app.get("/users/search")
def search_users(q: str = ""):
    results = []
    for u in users_db:
        if q.lower() in u["username"].lower():
            results.append({"id": u["id"], "username": u["username"]})
    return results

@app.get("/")
def root():
    return {"message": "User Service is running", "users_count": len(users_db)}