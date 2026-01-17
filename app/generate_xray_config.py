from vars import xray_uuid, xray_path
from string import Template

xray_config_template = "./templates/xray_config_template.json"
xray_config_file = "./xray_config/xray_config.json"

def generate_xray_config():
    xray_config_substitute_values = {
        "xray_uuid": xray_uuid,
        "xray_path": xray_path
    }

    with open(xray_config_template, 'r') as file:
        xray_config = file.read()
        xray_config_filled = Template(xray_config).substitute(xray_config_substitute_values)

    with open(xray_config_file, 'w') as file:
        file.write(xray_config_filled)