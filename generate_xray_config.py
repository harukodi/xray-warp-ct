import json
from vars import xray_uuid, xray_path, enable_ipv6, enable_warp
from warp_class import Warp

xray_config_output_file = "./xray_config/xray_config.json"
xray_config_template = "./templates/xray_config_template.json"
xray_warp_template = "./templates/xray_warp_template.json"

def update_json_keys(data, keys_to_update):
    if isinstance(data, dict):
        result = {}
        for key, value in data.items():
            if key in keys_to_update:
                result[key] = keys_to_update[key]
            elif isinstance(value, (dict, list)):
                result[key] = update_json_keys(value, keys_to_update)
            else:
                result[key] = value
        return result
    elif isinstance(data, list):
        return [update_json_keys(item, keys_to_update) for item in data]
    else:
        return data

def handle_xray_json_files(input_file: str = None, output_file: str = None, keys_to_update: dict[str, any] = None, append_warp_data: dict[str, any] = None):
    if input_file and output_file and keys_to_update:
        with open(input_file, "r") as file_input:
            data = json.load(file_input)
        with open(output_file, "w") as file_output:
            json.dump(update_json_keys(data, keys_to_update), file_output, indent=4)

    elif input_file and output_file and append_warp_data:
        with open(input_file, "r") as file_input:
            data = json.load(file_input)
        data["outbounds"].insert(0, append_warp_data)
        with open(output_file, "w") as file_output:
            json.dump(data, file_output, indent=4)
            
    else:
        with open(input_file, "r") as file_input:
            data = json.load(file_input)
        return data
            
def generate_warp_config():
    private_key = Warp.warp_private_key()
    public_key = Warp.warp_public_key()
    
    if enable_ipv6.lower() == "true":
        warp_addresses = [Warp.warp_ipv4(), Warp.warp_ipv6()]
    else:
        warp_addresses = [Warp.warp_ipv4()]

    xray_warp_config_keys = {
        "secretKey": private_key,
        "address": warp_addresses,
        "publicKey": public_key
    }

    warp_config_data = update_json_keys(
        handle_xray_json_files(xray_warp_template), 
        keys_to_update=xray_warp_config_keys
    )
    return warp_config_data

def generate_xray_config():
    xray_config_keys = {
        "id": f"{xray_uuid}",
        "path": f"{xray_path}"
    }
    handle_xray_json_files(xray_config_template, xray_config_output_file, xray_config_keys)
    if enable_warp.lower() == "true":
        warp_config = generate_warp_config()
        handle_xray_json_files(xray_config_output_file, xray_config_output_file, append_warp_data=warp_config)