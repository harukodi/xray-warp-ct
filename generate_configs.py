import json, uuid, string, random, segno
from vars import domain_name, cloudflare_auth_token, xray_uuid, xray_path
from warp_class import Warp

def load_xray_json_data():
    global xray_json_data
    with open("./templates/xray_template.json", "r") as xray_config:
        xray_json_data = json.load(xray_config)

def load_warp_json_data():
    global warp_json_data
    with open("./templates/xray_warp_template.json", "r") as warp_config:
        warp_json_data = json.load(warp_config)

def load_caddy_json_data():
    global caddy_json_data
    with open("./templates/caddyfile_template.json", "r") as caddyfile:
        caddy_json_data = json.load(caddyfile)

def generate_xray_config():
    load_xray_json_data()
    load_warp_json_data()
    XRAY_SETTINGS_UUID = xray_json_data['inbounds'][0]['settings']['clients'][0]
    XRAY_SETTINGS_UUID['id'] = xray_uuid
    XRAY_STREAMSETTINGS_XHTTP = xray_json_data['inbounds'][0]['streamSettings']['xhttpSettings']
    XRAY_STREAMSETTINGS_XHTTP['path'] = xray_path
    warp_addresses = [Warp.warp_ipv4(), Warp.warp_ipv6()]
    warp_json_data['settings']['secretKey'] = Warp.warp_private_key()
    warp_json_data['settings']['address'] = warp_addresses
    warp_json_data['settings']['peers'][0]['publicKey'] = Warp.warp_public_key()
    xray_json_data['outbounds'].insert(0, warp_json_data)
    with open("./xray_config/xray_config.json", "w") as xray_config:
        json.dump(xray_json_data, xray_config, indent=4)

## Caddy config code
def generate_caddy_config():
    load_caddy_json_data()
    caddy_domain_name = caddy_json_data['apps']['http']['servers']['srv0']['routes'][0]['match'][0]
    caddy_domain_name['host'] = [f"{domain_name}"]
    caddy_tls_sni = caddy_json_data['apps']['http']['servers']['srv0']['tls_connection_policies'][0]['match']
    caddy_tls_sni['sni'] = [f"{domain_name}"]
    caddy_tls_subject = caddy_json_data['apps']['tls']['automation']['policies'][0]
    caddy_tls_subject['subjects'] = [f"{domain_name}"]
    caddy_proxy_path = caddy_json_data['apps']['http']['servers']['srv0']['routes'][0]['handle'][0]['routes'][0]['handle'][0]['routes'][0]['match'][0]
    caddy_proxy_path['path'] = [f"/{xray_path}/*"]
    caddy_match_path = caddy_json_data['apps']['http']['servers']['srv0']['routes'][0]['handle'][0]['routes'][0]['match'][0]
    caddy_match_path['path'] = [f"/{xray_path}/*"]
    caddy_cloudflare_auth_token = caddy_json_data['apps']['tls']['automation']['policies'][0]['issuers'][0]['challenges']['dns']['provider']
    caddy_cloudflare_auth_token['api_token'] = f"{cloudflare_auth_token}"
    with open("./caddy_config/caddyfile.json", "w") as caddyfile:
        json.dump(caddy_json_data, caddyfile, indent=4)