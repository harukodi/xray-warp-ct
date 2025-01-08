from os import environ
import uuid, string, random

xray_uuid = str(uuid.uuid4())
xray_path = ''.join(random.choices(string.ascii_uppercase + string.ascii_lowercase, k=38))
domain_name = environ.get("DOMAIN_NAME", "test.test.test")
port = environ.get("PORT", "443")
fingerprint = environ.get("FINGERPRINT", "chrome")
xray_version = environ.get("XRAY_VERSION", "latest")
wgcf_version = environ.get("WGCF_VERSION", "latest")
cloudflare_auth_token = environ.get("CLOUDFLARE_AUTH_TOKEN")
enable_caddy_log = environ.get("ENABLE_CADDY_LOG", "False")