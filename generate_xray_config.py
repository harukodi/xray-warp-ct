import json
from vars import xray_uuid, xray_path, enable_ipv6
from warp_class import Warp

def load_xray_json_data():
    global xray_json_data
    with open("./templates/xray_template.json", "r") as xray_config:
        xray_json_data = json.load(xray_config)

def load_warp_json_data():
    global warp_json_data
    with open("./templates/xray_warp_template.json", "r") as warp_config:
        warp_json_data = json.load(warp_config)

def generate_xray_config():
    load_xray_json_data()
    load_warp_json_data()
    XRAY_SETTINGS_UUID = xray_json_data['inbounds'][0]['settings']['clients'][0]
    XRAY_SETTINGS_UUID['id'] = xray_uuid
    XRAY_STREAMSETTINGS_XHTTP = xray_json_data['inbounds'][0]['streamSettings']['xhttpSettings']
    XRAY_STREAMSETTINGS_XHTTP['path'] = xray_path
    if enable_ipv6.lower() == "true":
        warp_addresses = [Warp.warp_ipv4(), Warp.warp_ipv6()]
    else:
        warp_addresses = [Warp.warp_ipv4()]
    warp_json_data['settings']['secretKey'] = Warp.warp_private_key()
    warp_json_data['settings']['address'] = warp_addresses
    warp_json_data['settings']['peers'][0]['publicKey'] = Warp.warp_public_key()
    xray_json_data['outbounds'].insert(0, warp_json_data)
    with open("./xray_config/xray_config.json", "w") as xray_config:
        json.dump(xray_json_data, xray_config, indent=4)