import json, platform, subprocess
import urllib.error
from urllib.request import urlretrieve
from urllib.request import urlopen
from vars import wgcf_version

arch_platform = platform.machine()
wgcf_path = "./wgcf"

def chmod_wgcf():
    subprocess.run(["chmod", "+x", f"{wgcf_path}/wgcf"], stderr=subprocess.DEVNULL, stdout=subprocess.DEVNULL)

def fetch_latest_wgcf_version_tag():
    wgcf_tags_url = "https://api.github.com/repos/ViRb3/wgcf/tags"
    response = urlopen(wgcf_tags_url)
    wgcf_latest_version_tag = f"{json.loads(response.read().decode('utf-8'))[0]['name']}"
    wgcf_latest_version_tag_formatted = wgcf_latest_version_tag.replace("v", "")
    return wgcf_latest_version_tag_formatted

def download_wgcf_binary(version):
    if arch_platform in ["AMD64", "x86_64"]:
        wgcf_base_url = f"https://github.com/ViRb3/wgcf/releases/download/v{version}/wgcf_{version}_linux_amd64"
    if arch_platform in ["aarch64"]:
        wgcf_base_url = f"https://github.com/ViRb3/wgcf/releases/download/v{version}/wgcf_{version}_linux_arm64"
    try:
        urlretrieve(wgcf_base_url, f"{wgcf_path}/wgcf")
        if arch_platform in ["AMD64", "x86_64"]:
            print(f"Wgcf: {version} x86_64")
        if arch_platform in ["aarch64"]:
            print(f"Wgcf: {version} aarch64")
    except (urllib.error.HTTPError, urllib.error.URLError) as e:
        print(f"Wgcf-binary: failed to download, error: {e.reason}")

def setup_wgcf():
    if wgcf_version.lower() != "latest":
        download_wgcf_binary(wgcf_version)
    else:
        download_wgcf_binary(fetch_latest_wgcf_version_tag())
    chmod_wgcf()