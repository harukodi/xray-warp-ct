import uuid, string, random
from os import environ
from dotenv import load_dotenv
load_dotenv(override=True)

xray_uuid = environ.get("XRAY_UUID", str(uuid.uuid4()))
xray_path = environ.get("XRAY_PATH", ''.join(random.choices(string.ascii_uppercase + string.ascii_lowercase, k=38)))
domain_name = environ.get("DOMAIN_NAME")
port = environ.get("PORT", "443")
fingerprint = environ.get("FINGERPRINT", "chrome")
xray_version = environ.get("XRAY_VERSION", "latest")
wgcf_version = environ.get("WGCF_VERSION", "latest")
cloudflare_auth_token = environ.get("CLOUDFLARE_AUTH_TOKEN")
enable_caddy_log = environ.get("ENABLE_CADDY_LOG", "False")
enable_warp = environ.get("ENABLE_WARP", "True")
enable_ipv6 = environ.get("ENABLE_IPV6", "False")