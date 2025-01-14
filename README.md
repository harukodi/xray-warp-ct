
## PREREQUISITES
* Docker and Docker-compose
* Non-root account
* Domain name on cloudflare
* Cloudflare auth token with the `Zone.DNS` permission

## Create docker-compose file and the needed folders
```bash
mkdir xray-warp && \
cd xray-warp && \
mkdir certs && \
mkdir -p config/{caddy_config,xray_config} && \
touch docker-compose.yaml
```

## Docker-compose file example
```yaml
services:
  xray-warp:
    image: xray-warp:latest
    container_name: xray-warp-ct
    user: 1000:1000
    ports:
      - '443:443'
    environment:
      - DOMAIN_NAME=subdomain.domain.tld
      - PORT=443
      - FINGERPRINT=chrome
      - XRAY_VERSION=24.12.31
      - WGCF_VERSION=2.2.24
      - CLOUDFLARE_AUTH_TOKEN=
      - ENABLE_CADDY_LOG=false
    volumes:
      - ./certs:/xray_base/caddy_certs
      - ./config/xray_config:/xray_base/xray_config
      - ./config/caddy_config:/xray_base/caddy_config
```

## File tree
```
📦xray-ct-test  
 ┣ 📂certs  
 ┣ 📂config  
 ┃ ┣ 📂caddy_config  
 ┃ ┗ 📂xray_config  
 ┗ 📜docker-compose.yaml
```

## Spin up the container
```bash
sudo docker-compose up -d
```