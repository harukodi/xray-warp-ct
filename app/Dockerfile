# Build caddy with cloudflare plugin
ARG PYTHON_VERSION=3.13.11-slim-trixie
ARG CADDY_BUILDER_VERSION=2.10.2-builder-alpine
ARG CADDY_SERVER_VERSION=2.10.2-alpine

# Build step for caddy web server
FROM caddy:${CADDY_BUILDER_VERSION} AS caddy_builder
RUN xcaddy build \
    --with github.com/caddy-dns/cloudflare
FROM caddy:${CADDY_SERVER_VERSION}

# Build the base image for the xray_xhttp container
FROM python:${PYTHON_VERSION}
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV DEBIAN_FRONTEND=noninteractive
ENV XDG_DATA_HOME=/xray_base/caddy_certs
EXPOSE 443/tcp
EXPOSE 443/udp
COPY --from=caddy_builder /usr/bin/caddy /usr/bin/caddy
COPY . /xray_base/
WORKDIR /xray_base

RUN --mount=type=cache,target=/root/.cache/pip \
    --mount=type=bind,source=requirements.txt,target=requirements.txt \
    python -m pip install -r requirements.txt

RUN apt update && apt install ca-certificates curl gnupg lsb-release libcap2-bin gosu dbus -y --no-install-recommends && \
    curl -fsSL https://pkg.cloudflareclient.com/pubkey.gpg | gpg --yes --dearmor --output /usr/share/keyrings/cloudflare-warp-archive-keyring.gpg && \
    echo "deb [signed-by=/usr/share/keyrings/cloudflare-warp-archive-keyring.gpg] https://pkg.cloudflareclient.com/ $(lsb_release -cs) main" | tee /etc/apt/sources.list.d/cloudflare-client.list && \
    apt update && apt install cloudflare-warp --no-install-recommends -y && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

RUN mkdir /xray_base/caddy_certs /run/dbus && \
    chmod +x /usr/bin/caddy && \
    setcap cap_net_bind_service=+ep /usr/bin/caddy && \
    mv entrypoint.sh /usr/local/bin && chmod +x /usr/local/bin/entrypoint.sh

ENTRYPOINT ["/usr/local/bin/entrypoint.sh"]