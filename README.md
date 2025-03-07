# Xray-Warp docker container

## Prerequisites
* Docker and Docker-compose
* Non-root account
* Domain name on cloudflare
* Cloudflare auth token with the `Zone.DNS EDIT` and `Zone.Zone READ` permissions

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
    image: xia1997x/xray-warp:latest
    container_name: xray-warp-ct
    user: 1000:1000
    ports:
      - '443:443'
    environment:
      - DOMAIN_NAME=subdomain.domain.tld
      - PORT=443
      - XRAY_VERSION=latest
      - WGCF_VERSION=2.2.24
      - CLOUDFLARE_AUTH_TOKEN=
      - ENABLE_CADDY_LOG=False
      - ENABLE_IPV6=False
    volumes:
      - ./certs:/xray_base/caddy_certs
      - ./config/xray_config:/xray_base/xray_config
      - ./config/caddy_config:/xray_base/caddy_config
```

### **ENVs:**
> `DOMAIN_NAME`
> - Creates the dns record for you on Cloudflare.
> - Sets your domain for the xray-warp container
> - Must be a subdomain in the format of `subdomain.domain.tld`
> - `Required`
>
> `PORT`
> - Used to set the port you want to use, if you change the port of the docker container. Keep in mind that the port inside of the docker container can not be changed.
> - `YOUR-CUSTOM-PORT:443`. 
> - This is also used to set the right port for the vless link
> - `Required`
> - Default `443`
>
> `XRAY_VERSION`
> - Used to fetch the `xray core`
> - Will now skip over pre-releases. 
> - To set a custom xray core version you can set the variable to `XRAY_VERSION=25.3.6`.
> - Default `latest`
>
> `WGCF_VERSION`
> - Used to fetch the `WGCF` cli tool to create the warp profile to use with xray core
> - Default `2.2.24`
> 
> `ENABLE_CADDY_LOG`
> - Can be set to `True` if you want the log output of caddy.
> - Default `False`
> 
> `CLOUDFLARE_AUTH_TOKEN`
> - Stores the Cloudflare API token required for authentication and the tls certificate creation.
> - `Required`
> 
> `ENABLE_IPV6`
> - Can be set to `True` if the vps supports ipv6.
> - Default `False`

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
### **NOTE:** After starting the container, you can find the VLESS link and QR code inside the `xray_config` folder.

Enjoying this project? Support me with a coffee! ☕️✨ 
Thanks for your support! 🙌 https://ko-fi.com/xia1997x⁠

Made with ❤️ in Sweden! By xia1997x