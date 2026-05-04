from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
import uuid
import hashlib
import subprocess
import os
import pickle

# ⚠️ VULNERABLE: Debug mode enabled
app = FastAPI(title="User Service", debug=True)

# ⚠️ VULNERABLE: Hardcoded secrets (Gitleaks + Bandit)
JWT_SECRET = "supersecretkey123"
DB_PASSWORD = "admin123"
AWS_SECRET_KEY = "wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY"
ADMIN_PASSWORD = "admin123!"
API_KEY = "sk-1234567890abcdef"

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

# ⚠️ VULNERABLE: Weak MD5 hash for passwords
def hash_password(password: str):
    return hashlib.md5(password.encode()).hexdigest()

@app.post("/register")
def register(user: UserRegister):
    for u in users_db:
        if u["username"] == user.username:
            raise HTTPException(status_code=400, detail="Username already exists")
    
    new_user = {
        "id": str(uuid.uuid4()),
        "username": user.username,
        "password": hash_password(user.password),
        "email": user.email
    }
    users_db.append(new_user)
    return {"message": "User registered successfully", "user_id": new_user["id"]}

@app.post("/login")
def login(user: UserLogin):
    for u in users_db:
        if u["username"] == user.username and u["password"] == hash_password(user.password):
            return {
                "message": "Login successful",
                "user_id": u["id"],
                "username": u["username"]
            }
    raise HTTPException(status_code=401, detail="Invalid credentials")

# ⚠️ VULNERABLE: Command injection via shell=True
@app.get("/users/debug")
def debug_user(username: str):
    result = subprocess.run(
        f"echo user: {username}", shell=True, capture_output=True
    )
    return {"output": result.stdout.decode()}

# ⚠️ VULNERABLE: SQL injection pattern
@app.get("/users/search")
def search_users(q: str = ""):
    query = f"SELECT * FROM users WHERE name LIKE '%{q}%'"
    results = []
    for u in users_db:
        if q.lower() in u["username"].lower():
            results.append({"id": u["id"], "username": u["username"]})
    return {"query": query, "results": results}

# ⚠️ VULNERABLE: Insecure deserialization (pickle)
@app.post("/users/import")
def import_user(data: dict):
    raw = data.get("payload", "")
    obj = pickle.loads(raw.encode()) if isinstance(raw, str) else raw
    return {"result": str(obj)}

# ⚠️ VULNERABLE: Command injection via os.system
@app.get("/admin/exec")
def exec_command(cmd: str):
    os.system(f"echo executing: {cmd}")
    return {"message": f"Executed: {cmd}"}

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


@app.get("/")
def root():
    return {"message": "User Service is running", "users_count": len(users_db)}
