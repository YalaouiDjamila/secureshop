FROM python:3.11-slim
FROM nginx:alpine
COPY nginx.conf /etc/nginx/nginx.conf
RUN addgroup -S appgroup && adduser -S appuser -G appgroup
USER appuser
HEALTHCHECK CMD curl --fail http://localhost:8000/health || exit 1