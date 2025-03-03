from urllib.parse import quote
from vars import domain_name, xray_uuid, xray_path ,port, fingerprint
import segno

encoded_remark = quote(domain_name, safe="")
vless_uri = f"vless://{xray_uuid}@{domain_name}:{port}?encryption=none&security=tls&sni={domain_name}&alpn=h3%2Ch2%2Chttp%2F1.1&fp={fingerprint}&type=xhttp&host={domain_name}&path={xray_path}&mode=auto#{encoded_remark}"

def generate_xray_qr_code():
    qr_code = segno.make_qr(vless_uri)
    qr_code.save("./xray_config/xray_client_qr_code.png", scale=8)

def write_vless_link_to_file():
    with open('./xray_config/vless_link.txt', 'w') as vless_link_file:
        vless_link_file.write(vless_uri)