from urllib.request import urlopen
from cloudflare import Cloudflare
from vars import cloudflare_auth_token

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

def fetch_cf_zone_id():
    zone_id = cf_client.zones.list().result[0].id
    return zone_id

def create_cf_dns_record(record_name):
    try:
        if verify_cf_api_token():
            cf_client.dns.records.create(
                zone_id=fetch_cf_zone_id(),
                content=fetch_public_ip(),
                name=record_name,
                proxied=True,
                type="A"
            )
            print(f"DNS record for {record_name} has been created.")
        else:
            print("Invalid Cloudflare API token or insufficient permissions.")
            exit()
    except Exception:
        print("This dns record already exists.")

create_cf_dns_record("xray.harus.cloud")