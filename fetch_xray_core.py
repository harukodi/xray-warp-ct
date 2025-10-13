import json, platform, subprocess
import urllib.error
from urllib.request import urlretrieve
from urllib.request import urlopen
from zipfile import ZipFile
from os import remove
from vars import xray_version

xray_core_path = "./xray_core"
arch_platform = platform.machine()

def chmod_xray_core():
    file_path="./xray_core/xray"
    subprocess.run(["chmod", "+x", file_path], stderr=subprocess.DEVNULL, stdout=subprocess.DEVNULL)

def fetch_latest_xray_version_tag():
    xray_releases_url = "https://api.github.com/repos/XTLS/Xray-core/releases"
    response = urlopen(xray_releases_url)
    json_data = json.loads(response.read().decode('utf-8'))
    for item in json_data:
        if not item['prerelease']:
            xray_tag = f"{item['tag_name']}"
            return xray_tag.replace("v", "")

def download_file(filename, version):
    xray_base_url = f"https://github.com/XTLS/Xray-core/releases/download/v{version}/{filename}"
    def unzip_xray_core(filename):
        with ZipFile(f"{xray_core_path}/{filename}", "r") as xray_zip_file:
            xray_zip_file.extractall(path=xray_core_path)
        for file in [f"{xray_core_path}/{filename}", f"{xray_core_path}/README.md"]: remove(file)
    try:
        urlretrieve(xray_base_url, f"{xray_core_path}/{filename}")
        unzip_xray_core(filename)
        if arch_platform in ["AMD64", "x86_64"]:
            print(f"Xray-core: {version} x86_64")
        if arch_platform in ["aarch64"]:
            print(f"Xray-core: {version} aarch64")
    except (urllib.error.HTTPError, urllib.error.URLError) as e:
        print(f"Xray-binary: failed to download, error: {e.reason}")
        print("Falling back to already installed Xray binary!")

def fetch_xray_core():
    if arch_platform in ["AMD64", "x86_64"]:
        xray_platform_zip = "Xray-linux-64.zip"
        if xray_version.lower() != "latest":
            download_file(xray_platform_zip, xray_version)
        else:
            xray_latest_version = fetch_latest_xray_version_tag()
            download_file(xray_platform_zip, xray_latest_version)
    
    if arch_platform in ["aarch64"]:
        xray_platform_zip = "Xray-linux-arm64-v8a.zip"
        if xray_version.lower() != "latest":
            download_file(xray_platform_zip, xray_version)
        else:
            xray_latest_version = fetch_latest_xray_version_tag()
            download_file(xray_platform_zip, xray_latest_version)

fetch_xray_core()