import os.path, atexit, signal, sys
from fetch_xray_core import fetch_xray_core, chmod_xray_core
from fetch_wgcf import fetch_wgcf, chmod_wgcf
from generate_wgcf_profile import generate_wgcf_profile_and_register
from generate_xray_config import generate_xray_config
from generate_xray_qr_code_and_link import generate_xray_qr_code, write_vless_link_to_file
from generate_caddy_config import generate_caddy_config
from start_services import start_xray_core, start_caddy_server
from vars import xray_version, wgcf_version

files_to_check = [
    "./xray_config/xray_config.json",
    "./xray_config/xray_client_qr_code.png",
    "./xray_config/vless_link.txt",
    "./caddy_config/caddyfile.json"
]


def start_services():
    global xray_process, caddy_process
    xray_process = start_xray_core()
    caddy_process = start_caddy_server()

def initialize():
    fetch_wgcf(wgcf_version)
    fetch_xray_core(xray_version)
    chmod_wgcf()
    chmod_xray_core()
    generate_wgcf_profile_and_register()
    generate_xray_config()
    generate_xray_qr_code()
    write_vless_link_to_file()
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
    if all(not os.path.exists(file) for file in files_to_check):
        initialize()
    else:
        fetch_latest_xray_core_on_startup()
        chmod_xray_core()
    start_services()
    exit_function()

if __name__ == "__main__":
    main()