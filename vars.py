from os import environ
domain_name = environ.get("DOMAIN_NAME", "example.com")
port = environ.get("PORT", "443")
fingerprint = environ.get("FINGERPRINT", "chrome")
xray_version = environ.get("XRAY_VERSION", "latest")
wgcf_version = environ.get("WGCF_VERSION", "latest")
cloudflare_auth_token = environ.get("CLOUDFLARE_AUTH_TOKEN", "test")