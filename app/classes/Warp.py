import pty, subprocess, sys, os, pty

class Warp:
    @staticmethod
    def register():
        master, slave = pty.openpty()
        register_warp_result = subprocess.Popen(
            ["warp-cli", "registration", "new"],
            stdin=slave,
            stdout=slave,
            stderr=slave
        )
        os.close(slave)
        os.write(master, "yes\n".encode())
        register_warp_result.wait(timeout=10)
        os.close(master)
        
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
                "Supported modes are:\n  - " + "\n  - ".join(supported_modes)
            )
            sys.exit(1)

    @staticmethod
    def disconnect():
        disconnect_warp_result = subprocess.run(
            ["warp-cli", "disconnect"],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )
        
        if disconnect_warp_result.returncode == 0:
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