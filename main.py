import os.path, atexit, signal, sys
from generate_configs import generate_xray_config, generate_caddy_config
from fetch_xray_core import fetch_xray_core
from fetch_wgcf import fetch_wgcf
from generate_wgcf_profile import generate_wgcf_profile_and_register
from start_services import start_xray_core, start_caddy_server
from vars import xray_version, wgcf_version

def start_services():
    global xray_process, caddy_process
    xray_process = start_xray_core()
    caddy_process = start_caddy_server()

def initialize():
    fetch_wgcf(wgcf_version)
    fetch_xray_core(xray_version)
    generate_wgcf_profile_and_register()
    generate_xray_config()
    generate_caddy_config()

def fetch_latest_xray_core_on_startup():
    fetch_xray_core(xray_version)

def exit_function():
    def on_exit():
        xray_process.terminate()
        caddy_process.terminate()
    def handle_exit(signum, frame):
        sys.exit(0)
    atexit.register(on_exit)
    signal.signal(signal.SIGTERM, handle_exit)
    signal.signal(signal.SIGINT, handle_exit)
    signal.pause()

def main():
    if not os.path.exists("./xray_config/xray_config.json") and not os.path.exists("./xray_config/xray_client_qr_code.png") and not os.path.exists("./caddy_config/caddyfile.json"):
        initialize()
    else:
        fetch_latest_xray_core_on_startup()
    start_services()
    exit_function()

if __name__ == "__main__":
    main()