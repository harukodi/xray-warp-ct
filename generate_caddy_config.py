from vars import domain_name, cloudflare_auth_token, xray_path
import json

def load_caddy_json_data():
    global caddy_json_data
    with open("./templates/caddyfile_template.json", "r") as caddyfile:
        caddy_json_data = json.load(caddyfile)

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