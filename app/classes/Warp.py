import subprocess
import sys

class Warp:
    @staticmethod
    def register():
        register_warp_result = subprocess.run(
            ["warp-cli", "registration", "new"],
            input="y\n",
            text=True,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )

        if register_warp_result.returncode == 0:
            print("Warp was registered successfully!")
        else:
            print("Warp registration failed!")
            sys.exit(1)

    @staticmethod
    def unregister():
        unregister_warp_result = subprocess.run(
            ["warp-cli", "registration", "delete"],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )
        
        if unregister_warp_result.returncode == 0:
            print("Warp unregistered successfully!")

    @staticmethod
    def set_mode(warp_mode: str):
        supported_modes = ["warp", "warp+doh", "warp+dot"]
        set_warp_mode_result = subprocess.run(
            ["warp-cli", "mode", f"{warp_mode}"],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )
        if set_warp_mode_result.returncode == 0:
            print(f"Warp mode set to {warp_mode}")
        else:
            print(
                f"Error: Could not change Warp mode to '{warp_mode}'.\n"
                "Reason: The mode is either not supported or invalid.\n"
                "Supported modes are:\n  - " + "\n  - ".join(supported_modes)
            )
            sys.exit(1)

    @staticmethod
    def disconnect():
        subprocess.run(
            ["warp-cli", "disconnect"],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )
        print("Warp disconnected successfully!")

    @staticmethod
    def connect():
        connect_warp_result = subprocess.run(
            ["warp-cli", "connect"],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )
        
        if connect_warp_result.returncode != 0:
            print("Warp connection failed!")
            sys.exit(1)


Warp.register()
Warp.set_mode("warp+doh")
Warp.connect()
Warp.disconnect()
Warp.unregister()