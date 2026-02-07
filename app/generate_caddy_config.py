import os
from vars import domain_name, xray_path
from string import Template

caddyfile_template = "./templates/caddyfile_template"
caddyfile_file = "./caddy_config/Caddyfile"

def generate_caddy_config():
    caddyfile_substitute_values = {
        "domain_name": domain_name,
        "xray_path": xray_path  
    }

    with open(caddyfile_template, 'r') as file:
        caddyfile = file.read()
        caddyfile_filled = Template(caddyfile).substitute(caddyfile_substitute_values)

    if os.path.exists(caddyfile_file):
        return
    else:
        with open(caddyfile_file, 'w') as file:
            file.write(caddyfile_filled)