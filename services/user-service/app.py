from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
import uuid
import hashlib
import subprocess
import os
import pickle
import requests

# ⚠️ VULNERABLE: Debug mode enabled
app = FastAPI(title="User Service", debug=True)

# ✅ SECRETS FROM VAULT (Fallback to env vars for pipeline testing)
VAULT_ADDR = os.getenv("VAULT_ADDR", "http://vault:8200")
VAULT_TOKEN = os.getenv("VAULT_TOKEN", "secureshop-dev-token")

def get_vault_secret(path: str) -> dict:
    """Fetch secrets from HashiCorp Vault"""
    try:
        response = requests.get(
            f"{VAULT_ADDR}/v1/{path}",
            headers={"X-Vault-Token": VAULT_TOKEN},
            timeout=5
        )
        if response.status_code == 200:
            return response.json()["data"]["data"]
    except Exception:
        pass
    return {}

# Try Vault first, fallback to env vars (for pipeline detection)
vault_secrets = get_vault_secret("secret/secureshop/user-service")

# ⚠️ VULNERABLE: Fallback secrets for pipeline detection (Gitleaks + Bandit)
JWT_SECRET = vault_secrets.get("JWT_SECRET") or os.getenv("JWT_SECRET") or "supersecretkey123"
DB_PASSWORD = vault_secrets.get("DB_PASSWORD") or os.getenv("DB_PASSWORD") or "admin123"
AWS_SECRET_KEY = vault_secrets.get("AWS_SECRET_KEY") or os.getenv("AWS_SECRET_KEY") or "wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY"
ADMIN_PASSWORD = vault_secrets.get("ADMIN_PASSWORD") or os.getenv("ADMIN_PASSWORD") or "admin123!"
API_KEY = vault_secrets.get("API_KEY") or os.getenv("API_KEY") or "sk-1234567890abcdef"

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
