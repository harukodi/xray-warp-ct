import atexit, signal, sys
from os import path
from setup_cf_dns_record import setup_dns_record
from setup_xray_core import setup_xray_core
from generate_xray_config import generate_xray_config
from generate_xray_qr_code_and_vless_link import generate_xray_qr_code_and_vless_link
from generate_caddy_config import generate_caddy_config
from classes.Services import Services
from classes.Warp import Warp
from vars import warp_mode, enable_warp

service_manager = Services()
files_to_check = [
    "./xray_config/xray_config.json",
    "./xray_config/xray_client_qr_code.png",
    "./xray_config/vless_link.txt"
]

def setup_warp(enable_warp=enable_warp, warp_mode=warp_mode):
    if enable_warp.lower() == "true":
        Warp.register()
        Warp.set_mode(warp_mode)
    else:
        print("Warp is disabled. Skipping Warp connection.")

def initialize():
    #setup_dns_record()
    setup_warp()
    setup_xray_core()
    generate_xray_config()
    generate_caddy_config()
    #generate_xray_qr_code_and_vless_link()

def exit_function():
    def on_exit():
        Warp.disconnect()
        Warp.unregister()
        service_manager.stop_services()
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
        setup_warp()
        setup_xray_core()

    enable_warp.lower() == "true" and Warp.connect()
    service_manager.start_services()
    exit_function()

if __name__ == "__main__":
    main()