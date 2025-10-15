# Build caddy with cloudflare plugin
ARG PYTHON_VERSION=3.13.2-alpine3.21
ARG CADDY_BUILDER_VERSION=2.10.2-builder-alpine
ARG CADDY_SERVER_VERSION=2.10.2-alpine
FROM caddy:${CADDY_BUILDER_VERSION} AS builder
RUN xcaddy build \
    --with github.com/caddy-dns/cloudflare
FROM caddy:${CADDY_SERVER_VERSION}

# Build the base image for the xray_xhttp container
FROM python:${PYTHON_VERSION}
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV XDG_DATA_HOME=/xray_base/caddy_certs
EXPOSE 443/tcp
EXPOSE 443/udp
COPY --from=builder /usr/bin/caddy /usr/bin/caddy
WORKDIR /xray_base
COPY . /xray_base/
RUN addgroup -S xray_group && adduser -S xray_user -G xray_group
RUN mkdir /xray_base/caddy_certs && \
    chmod +x /usr/bin/caddy && \
    apk update && apk add --no-cache libcap && \
    setcap cap_net_bind_service=+ep /usr/bin/caddy && \
    chown -R xray_user:xray_group /xray_base && \
    chmod -R o+rwx /xray_base/wgcf /xray_base/xray_config/xray_core && \
    rm -rf /var/cache/apk/*
RUN --mount=type=cache,target=/root/.cache/pip \
    --mount=type=bind,source=requirements.txt,target=requirements.txt \
    python -m pip install -r requirements.txt
USER xray_user
CMD ["python", "main.py"]