from vars import domain_name, xray_path
from string import Template

def generate_caddy_config():
    caddyfile_template = "./templates/caddyfile_template"
    caddyfile_substitute_values = {
        "domain_name": domain_name,
        "xray_path": xray_path  
    }

    with open(caddyfile_template, 'r') as file:
        caddyfile = file.read()
    caddyfile_filled = Template(caddyfile).substitute(caddyfile_substitute_values)

    caddy_config = "./caddy_config/Caddyfile"
    with open(caddy_config, 'w') as file:
        file.write(caddyfile_filled)