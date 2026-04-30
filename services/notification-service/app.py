from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI(title="Notification Service")

notifications_sent = []  # Store sent notifications

class Notification(BaseModel):
    user_id: str
    message: str
    type: str  # email or sms

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