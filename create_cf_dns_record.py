import sys
from urllib.request import urlopen
from cloudflare import Cloudflare
from vars import cloudflare_auth_token, domain_name

cf_client = Cloudflare(
    api_token=cloudflare_auth_token
)

def verify_cf_api_token():
    try:
        cf_client.user.tokens.verify()
        return True
    except Exception:
        return False

def fetch_public_ip():
    ip_api_endpoint = "https://checkip.amazonaws.com/"
    response = urlopen(ip_api_endpoint)
    ip_data = response.read().decode("utf-8").strip()
    return ip_data

def fetch_cf_zone_id(dns_record_name):
    main_domain_name = ".".join(dns_record_name.split(".")[-2:])
    zone_ids = cf_client.zones.list()
    for zone_id in zone_ids:
        if zone_id.name == main_domain_name:
            return zone_id.id

def create_cf_dns_record():
    try:
        if verify_cf_api_token():
            cf_client.dns.records.create(
                zone_id=fetch_cf_zone_id(domain_name),
                content=fetch_public_ip(),
                name=domain_name,
                proxied=True,
                type="A"
            )
            print(f"DNS record for {domain_name} has been created.")
        else:
            print("Invalid Cloudflare API token or insufficient permissions.")
            sys.exit(1)
    except Exception:
        print("This dns record already exists.")