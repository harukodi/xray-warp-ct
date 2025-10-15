import atexit, signal, sys
from os import path
from create_cf_dns_record import create_cf_dns_record
from setup_xray_core import setup_xray_core
from setup_wgcf import setup_wgcf
from generate_wgcf_profile import generate_wgcf_profile_and_register
from generate_xray_config import generate_xray_config
from generate_xray_qr_code_and_vless_link import generate_xray_qr_code_and_vless_link
from generate_caddy_config import generate_caddy_config
from start_services import start_xray_core, start_caddy_server

files_to_check = [
    "./caddy_config/Caddyfile",
    "./xray_config/xray_config.json",
    "./xray_config/xray_client_qr_code.png",
    "./xray_config/vless_link.txt"
]


def start_services():
    global xray_process, caddy_process
    xray_process = start_xray_core()
    caddy_process = start_caddy_server()

def initialize():
    #create_cf_dns_record()
    setup_wgcf()
    setup_xray_core()
    generate_wgcf_profile_and_register()
    generate_xray_config()
    generate_caddy_config()
    generate_xray_qr_code_and_vless_link()

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
    if all(not path.exists(file) for file in files_to_check):
        initialize()
    else:
        setup_xray_core()
    start_services()
    exit_function()

if __name__ == "__main__":
    main()