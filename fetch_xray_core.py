from urllib.request import urlretrieve
from urllib.request import urlopen
import json, platform, subprocess
from zipfile import ZipFile
from os import remove
from vars import xray_version

def chmod_xray_core():
    file_path="./xray_core/xray"
    subprocess.run(["chmod", "+x", file_path], stderr=subprocess.DEVNULL, stdout=subprocess.DEVNULL)

def fetch_latest_xray_version():
    xray_releases_url = "https://api.github.com/repos/XTLS/Xray-core/releases"
    response = urlopen(xray_releases_url)
    json_data = json.loads(response.read().decode('utf-8'))
    for item in json_data:
        if not item['prerelease']:
            return item['tag_name']

def unzip_xray_core(xray_platform_zip_file):
    xray_core_path = "./xray_core"
    with ZipFile(f"{xray_core_path}/{xray_platform_zip_file}", "r") as xray_zip_file:
        xray_zip_file.extractall(path=xray_core_path)
    remove(f"{xray_core_path}/{xray_platform_zip_file}")

def fetch_xray_core(version):
    arch_platform = platform.machine()
    if arch_platform in ["AMD64", "x86_64"]:
        xray_platform_zip = "Xray-linux-64.zip"
        if xray_version.lower() != "latest":
            xray_url = f"https://github.com/XTLS/Xray-core/releases/download/v{version}/{xray_platform_zip}"
            xray_core_path = f"./xray_core/{xray_platform_zip}"
            urlretrieve(xray_url, xray_core_path)
            unzip_xray_core(xray_platform_zip)
            print(f"Xray-core: {version} x86_64")
        else:
            xray_latest_version = fetch_latest_xray_version()
            xray_url = f"https://github.com/XTLS/Xray-core/releases/download/{xray_latest_version}/{xray_platform_zip}"
            xray_core_path = f"./xray_core/{xray_platform_zip}"
            urlretrieve(xray_url, xray_core_path)
            unzip_xray_core(xray_platform_zip)
            print(f"Xray-core: {xray_latest_version} x86_64")
    
    if arch_platform in ["aarch64"]:
        xray_platform_zip = "Xray-linux-arm64-v8a.zip"
        if xray_version.lower() != "latest":
            xray_url = f"https://github.com/XTLS/Xray-core/releases/download/v{version}/{xray_platform_zip}"
            xray_core_path = f"./xray_core/{xray_platform_zip}"
            urlretrieve(xray_url, xray_core_path)
            unzip_xray_core(xray_platform_zip)
            print(f"Xray-core: {version} aarch64")
        else:
            xray_latest_version = fetch_latest_xray_version()
            xray_url = f"https://github.com/XTLS/Xray-core/releases/download/{xray_latest_version}/{xray_platform_zip}"
            xray_core_path = f"./xray_core/{xray_platform_zip}"
            urlretrieve(xray_url, xray_core_path)
            unzip_xray_core(xray_platform_zip)
            print(f"Xray-core: {xray_latest_version} aarch64")