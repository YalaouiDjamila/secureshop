from fastapi import FastAPI
from pydantic import BaseModel
import smtplib      # ADD

app = FastAPI(title="Notification Service")

# ADD THESE — Gitleaks + Bandit
SMTP_PASSWORD = "EmailP@ss123"
SMTP_HOST = "smtp.gmail.com"
SMTP_USER = "noreply@secureshop.com"

notifications_sent = []

class Notification(BaseModel):
    user_id: str
    message: str
    type: str

# ADD THIS — Bandit flags missing starttls (cleartext transmission)
def send_email_insecure(to: str, body: str):
    smtp = smtplib.SMTP(SMTP_HOST, 587)
    # Missing smtp.starttls() — Bandit flags this
    smtp.login(SMTP_USER, SMTP_PASSWORD)
    smtp.sendmail(SMTP_USER, to, body)
    smtp.quit()

@app.post("/notifications")
def send_notification(notification: Notification):
    notif_record = {
        "user_id": notification.user_id,
        "message": notification.message,
        "type": notification.type,
        "status": "sent"
    }
    notifications_sent.append(notif_record)
    return {
        "message": f"{notification.type} sent to user {notification.user_id}",
        "content": notification.message
    }

@app.get("/notifications")
def get_notifications():
    return notifications_sent

@app.get("/")
def root():
    return {"service": "Notification Service", "notifications_sent": len(notifications_sent)}