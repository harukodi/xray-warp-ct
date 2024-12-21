import subprocess

def generate_wgcf_profile_and_register():
    subprocess.run(["./wgcf/wgcf", "register", "--accept-tos", "--config", "./wgcf/wgcf-account.toml"], stderr=subprocess.DEVNULL, stdout=subprocess.DEVNULL)
    subprocess.run(["./wgcf/wgcf", "generate", "--config", "./wgcf/wgcf-account.toml", "--profile", "./wgcf/wgcf-profile.conf"], capture_output=False)