from urllib.request import urlretrieve
from urllib.request import urlopen
import json, platform, subprocess
from vars import wgcf_version

def chmod_wgcf():
    file_path="./wgcf/wgcf"
    subprocess.run(["chmod", "+x", file_path], stderr=subprocess.DEVNULL, stdout=subprocess.DEVNULL)

def fetch_latest_wgcf_version_tag():
    wgcf_tags_url = "https://api.github.com/repos/ViRb3/wgcf/tags"
    response = urlopen(wgcf_tags_url)
    json_data = json.loads(response.read().decode('utf-8'))
    wgcf_latest_version = json_data[0]['name']
    return wgcf_latest_version

def fetch_wgcf():
    arch_platform = platform.machine()
    if arch_platform in ["AMD64", "x86_64"]:
        if wgcf_version.lower() != "latest":
            wgcf_url = f"https://github.com/ViRb3/wgcf/releases/download/v{wgcf_version}/wgcf_{wgcf_version}_linux_amd64"
            wgcf_path = f"./wgcf/wgcf"
            urlretrieve(wgcf_url, wgcf_path)
            print(f"Wgcf: v{wgcf_version} x86_64")
        else:
            wgcf_latest_version = fetch_latest_wgcf_version_tag()
            wgcf_latest_version_formated = wgcf_latest_version.replace('v', '')
            wgcf_url = f"https://github.com/ViRb3/wgcf/releases/download/{wgcf_latest_version}/wgcf_{wgcf_latest_version_formated}_linux_amd64"
            wgcf_path = f"./wgcf/wgcf"
            urlretrieve(wgcf_url, wgcf_path)
            print(f"Wgcf: {wgcf_latest_version_formated} x86_64")

    if arch_platform in ["aarch64"]:
        if wgcf_version.lower() != "latest":
            wgcf_url = f"https://github.com/ViRb3/wgcf/releases/download/v{wgcf_version}/wgcf_{wgcf_version}_linux_arm64"
            wgcf_path = f"./wgcf/wgcf"
            urlretrieve(wgcf_url, wgcf_path)
            print(f"Wgcf: v{wgcf_version} aarch64")
        else:
            wgcf_latest_version = fetch_latest_wgcf_version_tag()
            wgcf_latest_version_formated = wgcf_latest_version.replace('v', '')
            wgcf_url = f"https://github.com/ViRb3/wgcf/releases/download/{wgcf_latest_version}/wgcf_{wgcf_latest_version_formated}_linux_arm64"
            wgcf_path = f"./wgcf/wgcf"
            urlretrieve(wgcf_url, wgcf_path)
            print(f"Wgcf: v{wgcf_latest_version_formated} aarch64")

fetch_wgcf()