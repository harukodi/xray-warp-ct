import os.path
from generate_configs import generate_xray_config, generate_caddy_config
from fetch_xray_core import fetch_xray_core
from fetch_wgcf import fetch_wgcf
from generate_wgcf_profile import generate_wgcf_profile_and_register
from start_services import start_xray_core, start_caddy_server
from vars import xray_version, wgcf_version

def initialize():
    fetch_wgcf(wgcf_version)
    fetch_xray_core(xray_version)
    generate_wgcf_profile_and_register()
    generate_xray_config()
    generate_caddy_config()
    start_xray_core()
    #start_caddy_server()

def startup():
    fetch_xray_core(xray_version)
    start_xray_core()
    #start_caddy_server()

def main():
    if not os.path.exists("./xray_config/xray_config.json") and not os.path.exists("./xray_config/xray_client_qr_code.png") and not os.path.exists("./caddy_config/caddyfile.json"):
        initialize()
    else:
        startup()

if __name__ == "__main__":
    main()