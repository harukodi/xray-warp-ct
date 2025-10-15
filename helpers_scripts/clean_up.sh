files_to_remove=(
    "caddy_config/*"
    "xray_config/xray_config.json"
    "xray_config/vless_link.txt"
    "xray_config/xray_client_qr_code.png"
    "xray_config/xray_core/*"
    "wgcf/*"
)

function remove_file () {
    file_to_remove="$1"
    rm -f $file_to_remove
}

for file in "${files_to_remove[@]}"
do
    remove_file "$file"
done