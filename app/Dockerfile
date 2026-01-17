# Build caddy with cloudflare plugin
ARG PYTHON_VERSION=3.14.2-slim-trixie
ARG WARP_CLI_INSTALLER_VERSION=trixie
ARG CADDY_BUILDER_VERSION=2.10.2-builder-alpine
ARG CADDY_SERVER_VERSION=2.10.2-alpine

# Build step for caddy web server
FROM caddy:${CADDY_BUILDER_VERSION} AS caddy_builder
RUN xcaddy build \
    --with github.com/caddy-dns/cloudflare
FROM caddy:${CADDY_SERVER_VERSION}

# Installation step of the warp_cli tool
FROM debian:${WARP_CLI_INSTALLER_VERSION} AS warp_cli_installer
RUN apt update && apt upgrade -y && apt install ca-certificates curl gnupg2 lsb-release libcap2-bin -y
RUN curl -fsSL https://pkg.cloudflareclient.com/pubkey.gpg | gpg --yes --dearmor --output /usr/share/keyrings/cloudflare-warp-archive-keyring.gpg && \
    echo "deb [signed-by=/usr/share/keyrings/cloudflare-warp-archive-keyring.gpg] https://pkg.cloudflareclient.com/ $(lsb_release -cs) main" | tee /etc/apt/sources.list.d/cloudflare-client.list && \
    apt update && apt install cloudflare-warp -y

# Build the base image for the xray_xhttp container
FROM python:${PYTHON_VERSION}
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV XDG_DATA_HOME=/xray_base/caddy_certs
EXPOSE 443/tcp
EXPOSE 443/udp
COPY --from=caddy_builder /usr/bin/caddy /usr/bin/caddy
COPY --from=warp_cli_installer /usr/bin/warp-cli /usr/bin/warp-cli
WORKDIR /xray_base
COPY . /xray_base/
RUN apt update && apt install libcap2-bin -y --no-install-recommends && rm -rf /var/lib/apt/lists/*
RUN --mount=type=cache,target=/root/.cache/pip \
    --mount=type=bind,source=requirements.txt,target=requirements.txt \
    python -m pip install -r requirements.txt
RUN mkdir /xray_base/caddy_certs && \
    chmod +x /usr/bin/caddy && \
    chmod +x /usr/bin/warp-cli && \
    setcap cap_net_bind_service=+ep /usr/bin/caddy && \
    groupadd -r xray_group && useradd -r -g xray_group -s /bin/bash xray_user && \
    chown -R xray_user:xray_group /xray_base && \
    chmod -R o+rwx /xray_base/xray_config/xray_core

USER xray_user
CMD ["python", "main.py"]