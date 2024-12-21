import json, uuid, string, random, segno
from vars import domain_name, port, fingerprint
from warp_class import Warp
from urllib.parse import quote

xray_uuid = None
xray_servicename = None

def load_xray_json_data():
    global xray_json_data
    with open("./templates/xray_template.json", "r") as xray_config:
        xray_json_data = json.load(xray_config)

def load_warp_json_data():
    global warp_json_data
    with open("./templates/xray_warp_template.json", "r") as warp_config:
        warp_json_data = json.load(warp_config)

def generate_random_string_and_uuid():
    global xray_uuid, xray_servicename
    random_xray_uuid = str(uuid.uuid4())
    random_xray_servicename = ''.join(random.choices(string.ascii_uppercase + string.ascii_lowercase, k=38))
    xray_uuid = random_xray_uuid
    xray_servicename = random_xray_servicename

def generate_xray_qr_code(uuid, domain, port, service_name, fingerprint):
    encoded_remark = quote(domain, safe="")
    vless_uri = f"vless://{uuid}@{domain}:{port}?encryption=none&security=tls&sni={domain}&alpn=h3%2Ch2%2Chttp%2F1.1&fp={fingerprint}&type=grpc&authority={domain}&serviceName={service_name}&mode=gun#xia1997x: {encoded_remark}"
    qr_code = segno.make_qr(vless_uri)
    qr_code.save("./xray_config/xray_client_qr_code.png", scale=8)

def generate_xray_config():
    load_xray_json_data()
    load_warp_json_data()
    generate_random_string_and_uuid()
    generate_xray_qr_code(xray_uuid, domain_name, port, xray_servicename, fingerprint)
    XRAY_SETTINGS_UUID = xray_json_data['inbounds'][0]['settings']['clients'][0]
    XRAY_SETTINGS_UUID['id'] = xray_uuid
    XRAY_STREAMSETTINGS_SERVICENAME = xray_json_data['inbounds'][0]['streamSettings']['grpcSettings']
    XRAY_STREAMSETTINGS_SERVICENAME["serviceName"] = xray_servicename
    warp_addresses = [Warp.warp_ipv4(), Warp.warp_ipv6()]
    warp_json_data['settings']['secretKey'] = Warp.warp_private_key()
    warp_json_data['settings']['address'] = warp_addresses
    warp_json_data['settings']['peers'][0]['publicKey'] = Warp.warp_public_key()
    xray_json_data['outbounds'].insert(0, warp_json_data)
    with open("./xray_config/xray_config.json", "w") as xray_config:
        json.dump(xray_json_data, xray_config, indent=4)


## Caddy config code
def load_caddy_json_data():
    global caddy_json_data
    with open("./templates/caddyfile_template.json", "r") as caddyfile:
        caddy_json_data = json.load(caddyfile)

def generate_caddy_config():
    load_caddy_json_data()
    # Sets the domain name
    caddy_domain_name = caddy_json_data['apps']['http']['servers']['srv0']['routes'][0]['match'][0]
    caddy_domain_name['host'] = f"{domain_name}"
    # Sets the tls sni
    caddy_tls_sni = caddy_json_data['apps']['http']['servers']['srv0']['tls_connection_policies'][0]['match']
    caddy_tls_sni['sni'] = f"{domain_name}"
    # Sets the tls subject
    caddy_tls_subject = caddy_json_data['apps']['tls']['automation']['policies'][0]
    caddy_tls_subject['subjects'] = f"{domain_name}"
    # Sets the proxy path to the service
    caddy_proxy_path = caddy_json_data['apps']['http']['servers']['srv0']['routes'][0]['handle'][0]['routes'][0]['handle'][0]['routes'][0]['match'][0]
    caddy_proxy_path['path'] = f"/{xray_servicename}/*"
    # Sets the match path for the handle
    caddy_match_path = caddy_json_data['apps']['http']['servers']['srv0']['routes'][0]['handle'][0]['routes'][0]['match'][0]
    caddy_match_path['path'] = f"/{xray_servicename}/*"
    # Saves the dynamic config file
    with open("./caddy_config/caddyfile.json", "w") as caddyfile:
        json.dump(caddy_json_data, caddyfile, indent=4)