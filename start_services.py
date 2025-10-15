import subprocess
from vars import enable_caddy_log

caddyfile_path = "./caddy_config"
xray_config_path = "./xray_config"
xray_core_path = "./xray_config/xray_core"

def start_caddy_server():
    if enable_caddy_log.lower() == "true":
        return subprocess.Popen(["caddy", "run", "--config", f"{caddyfile_path}/Caddyfile"])
    else:
        return subprocess.Popen(["caddy", "run", "--config", f"{caddyfile_path}/Caddyfile"], stderr=subprocess.DEVNULL, stdout=subprocess.DEVNULL)

def start_xray_core():
    return subprocess.Popen([f"{xray_core_path}/xray", "run", "-c", f"{xray_config_path}/xray_config.json"])