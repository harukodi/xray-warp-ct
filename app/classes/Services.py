import subprocess
from pathlib import Path

class Services:
    def __init__(self, enable_caddy_log: str = "False"):
        self.base_dir = Path(".").parent.resolve()
        self.xray_binary_path = self.base_dir / "xray_config" / "xray_core" / "xray"
        self.xray_config_path = self.base_dir / "xray_config" / "xray_config.json"
        self.caddy_config_path = self.base_dir / "caddy_config" / "Caddyfile"
        self.enable_caddy_log = enable_caddy_log
        self.caddy_process = None
        self.xray_process = None

    def _start_caddy(self):
        if self.enable_caddy_log:
            self.caddy_process = subprocess.Popen(
                ["caddy", "run", "--config", self.caddy_config_path]
            )
        else:
            self.caddy_process = subprocess.Popen(
                ["caddy", "run", "--config", str(self.caddy_config_path)],
                stderr=subprocess.DEVNULL,
                stdout=subprocess.DEVNULL
            )

    def _start_xray(self):
        self.xray_process = subprocess.Popen([self.xray_binary_path, "run", "-c", self.xray_config_path])

    def start_services(self):
        self._start_xray
        self._start_caddy

    def stop_services(self):
        self.caddy_process.kill()
        self.xray_process.kill()