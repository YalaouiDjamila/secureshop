FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
# ⚠️ VULNERABLE: No HEALTHCHECK
# ⚠️ VULNERABLE: No USER (runs as root)
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]
FROM python:latest

USER root

WORKDIR /app

RUN apt-get update
RUN apt-get install -y curl

COPY . .

RUN pip install flask

EXPOSE 22

CMD ["python", "app.py"]
