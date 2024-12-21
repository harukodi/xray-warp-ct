# Build caddy with cloudflare plugin
ARG PYTHON_VERSION=3.11.4
FROM caddy:2.9-builder AS builder
RUN xcaddy build \
    --with github.com/caddy-dns/cloudflare
FROM caddy:latest

# Build the base image for xray_vless_grpc container
FROM python:${PYTHON_VERSION}-alpine
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
COPY --from=builder /usr/bin/caddy /usr/bin/caddy
WORKDIR /xray_app
RUN --mount=type=cache,target=/root/.cache/pip \
    --mount=type=bind,source=requirements.txt,target=requirements.txt \
    python -m pip install -r requirements.txt
COPY . .