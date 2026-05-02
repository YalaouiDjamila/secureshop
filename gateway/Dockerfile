FROM nginx:alpine
COPY nginx.conf /etc/nginx/nginx.conf
RUN addgroup -S appgroup && adduser -S appuser -G appgroup
USER appuser
HEALTHCHECK --interval=30s CMD wget -q --spider http://localhost/ || exit 1
