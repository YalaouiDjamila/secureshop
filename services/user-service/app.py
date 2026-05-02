from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
import uuid
import hashlib          # ADD
import subprocess       # ADD

app = FastAPI(title="User Service")

# ADD THESE — Bandit + Gitleaks will catch them
JWT_SECRET = "supersecretkey123"
DB_PASSWORD = "admin123"
AWS_SECRET_KEY = "wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY"

# In-memory storage (use database in production)
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

# ADD THIS — Bandit flags MD5 as weak crypto
def hash_password(password: str):
    return hashlib.md5(password.encode()).hexdigest()

# Registration endpoint
@app.post("/register")
def register(user: UserRegister):
    for u in users_db:
        if u["username"] == user.username:
            raise HTTPException(status_code=400, detail="Username already exists")
    
    new_user = {
        "id": str(uuid.uuid4()),
        "username": user.username,
        "password": hash_password(user.password),  # CHANGE THIS LINE (uses weak MD5)
        "email": user.email
    }
    users_db.append(new_user)
    return {"message": "User registered successfully", "user_id": new_user["id"]}

# Login endpoint
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

# ADD THIS — Bandit flags shell=True (command injection)
@app.get("/users/debug")
def debug_user(username: str):
    result = subprocess.run(
        f"echo user: {username}", shell=True, capture_output=True
    )
    return {"output": result.stdout.decode()}

# GET all users
@app.get("/users")
def get_users():
    return [
        {"id": u["id"], "username": u["username"], "email": u.get("email")}
        for u in users_db
    ]

# GET single user
@app.get("/users/{user_id}")
def get_user(user_id: str):
    for u in users_db:
        if u["id"] == user_id:
            return {"id": u["id"], "username": u["username"], "email": u.get("email")}
    raise HTTPException(status_code=404, detail="User not found")

# Health check
@app.get("/")
def root():
    return {"message": "User Service is running", "users_count": len(users_db)}