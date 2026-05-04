#!/bin/bash
export VAULT_ADDR='http://127.0.0.1:8200'
export VAULT_TOKEN='secureshop-dev-token'

# Store secrets
vault kv put secret/secureshop/user-service \
  JWT_SECRET="supersecretkey123" \
  DB_PASSWORD="admin123" \
  AWS_SECRET_KEY="EXAMPLEKEY"

vault kv put secret/secureshop/payment-service \
  STRIPE_KEY="sk_live_xxx" \
  PAYMENT_DB_PASSWORD="P@ssw0rd2024!"

vault kv put secret/secureshop/notification-service \
  SMTP_PASSWORD="EmailP@ss123" \
  SMTP_USER="noreply@secureshop.com"

echo "✅ Vault secrets configured"