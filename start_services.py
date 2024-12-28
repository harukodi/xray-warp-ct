import subprocess

def start_caddy_server():
    return subprocess.Popen(["caddy", "run", "--config", "./caddy_config/caddyfile.json"], stderr=subprocess.DEVNULL, stdout=subprocess.DEVNULL)

def start_xray_core():
    return subprocess.Popen(["./xray_core/xray", "run", "-c", "./xray_config/xray_config.json"])