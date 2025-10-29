# xray-warp-ct docker container

## Prerequisites
* Docker and Docker-compose
* Non-root account
* Domain name on cloudflare
* Cloudflare auth token with the `Zone.DNS EDIT` and `Zone.Zone READ` permissions

## Create docker-compose file and the needed folders
```bash
mkdir xray-warp-ct && \
cd xray-warp-ct && \
mkdir -p config/{certs,caddy_config,xray_config/xray_core} && \
touch docker-compose.yaml && \
touch .env
```

## Docker-compose file example
```yaml
services:
  xray-warp:
    image: xia1997x/xray-warp:latest
    container_name: xray-warp-ct
    user: 1000:1000
    env_file:
      - .env
    ports:
      - '443:443'
    volumes:
      - ./config/certs:/xray_base/caddy_certs
      - ./config/xray_config:/xray_base/xray_config
      - ./config/xray_config/xray_core:/xray_base/xray_config/xray_core
      - ./config/caddy_config:/xray_base/caddy_config
```

## .env file example
```dotenv
DOMAIN_NAME=
CLOUDFLARE_AUTH_TOKEN=
PORT=443
#XRAY_UUID=
#XRAY_PATH=
ENABLE_CADDY_LOG=False
ENABLE_WARP=True
ENABLE_IPV6=False
XRAY_VERSION=latest
WGCF_VERSION=latest
```
### **ENVs:**
> `DOMAIN_NAME`
> - Domain name to use for the DNS record.
> - Must be a subdomain in the format of `subdomain.domain.tld`
> - `Required`
> 
> `CLOUDFLARE_AUTH_TOKEN`
> - Cloudflare API token required for DNS record and TLS certificate creation.
> - `Required`
>
> `PORT`
> - Sets the port you want to use, if you change the port of the Docker container. Keep in mind that the port inside the Docker container cannot be changed.
> - This is also used to set the right port for the VLESS link.
> - Format: `YOUR-CUSTOM-PORT:443`
> - Default: `443`
> - `Required`
>
> `XRAY_VERSION`
> - Used to fetch the `xray-core` binary.
> - To set a custom Xray version, use e.g., `XRAY_VERSION=25.3.6`.
> - Default: `latest`
> - `Required`
>
> `WGCF_VERSION`
> - Used to fetch the `WGCF` binary.
> - To set a custom WGCF version, use e.g., `WGCF_VERSION=2.2.29`.
> - Default: `latest`
> - `Required`
> 
> `ENABLE_CADDY_LOG`
> - Can be set to `True` to enable the log output of Caddy.
> - Default: `False`
> 
> `ENABLE_IPV6`
> - Can be set to `True` if the VPS supports IPv6.
> - Default: `False`
>
> `XRAY_UUID`
> - Optional. If set, this value will be used as the Xray UUID.
> - If not set (commented out or empty), the script will automatically generate a valid UUID.
> - **Not recommended** for normal use; primarily added for testing purposes.
>
> `XRAY_PATH`
> - Optional. If set, defines the custom path used by Xray.
> - If not set, the script will automatically generate a random path.
> - **Not recommended** for normal use; primarily added for testing purposes.


## File tree
```
📦xray-warp-ct
 ┣ 📂config
 ┃ ┣ 📂caddy_config
 ┃ ┣ 📂certs
 ┃ ┗ 📂xray_config
 ┃ ┃ ┗ 📂xray_core
 ┣ 📜.env
 ┗ 📜docker-compose.yaml
```

## Spin up the container
```bash
sudo docker-compose up -d
```
### **NOTE:** After starting the container, you can find the VLESS link and QR code inside the `xray_config` folder.

Enjoying this project? Support me with a coffee! ☕️✨ 
Thanks for your support! 🙌 https://ko-fi.com/xia1997x⁠

Made with ❤️ in Sweden! By xia1997x