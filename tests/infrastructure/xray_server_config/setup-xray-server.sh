#!/bin/bash
# This script is used to test the connectivity of the xray warp ct container
SCRIPT_DIR=$(dirname "$(readlink -f "$0")")
declare -A xray_config_values=(
    ["DOMAIN_NAME"]="$1" 
    ["XRAY_PATH"]="$2"
    ["XRAY_UUID"]="$3"
    ["CLOUDFLARE_AUTH_TOKEN"]="$4"
    ["XRAY_ENCRYPTION_KEY"]="$5"
    ["XRAY_DECRYPTION_KEY"]="$6"
)

function create_docker_volume_caddyfile_func () {
    local CADDY_DIR="$SCRIPT_DIR/config/caddy_config"
    mkdir -p "$CADDY_DIR"
}

function install_docker_tools () {
    # Add Docker's official GPG key
    sudo apt-get update
    sudo apt-get install ca-certificates curl -y
    sudo install -m 0755 -d /etc/apt/keyrings
    sudo curl -fsSL https://download.docker.com/linux/ubuntu/gpg -o /etc/apt/keyrings/docker.asc
    sudo chmod a+r /etc/apt/keyrings/docker.asc

    # Add the repository to Apt sources
    echo \
      "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.asc] https://download.docker.com/linux/ubuntu \
      $(. /etc/os-release && echo "${UBUNTU_CODENAME:-$VERSION_CODENAME}") stable" | \
      sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
    sudo apt-get update
    sudo apt-get install docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin -y
}

function copy_config_from_template_file_func () {
    local template_file="$1"
    local output_file="$2"
    cp $SCRIPT_DIR/$template_file $SCRIPT_DIR/$output_file
}

function substitute_values_for_config_file_helper_func () {
    local local_key="$1"
    local local_value="$2"
    local file_to_substitute="$3"
    sed -i "s/\${$local_key}/$local_value/g" $SCRIPT_DIR/$file_to_substitute
}

function substitute_values_for_config_files_func () {
    local file_to_substitute="$1"
    for key in "${!xray_config_values[@]}"
    do
        substitute_values_for_config_file_helper_func "$key" "${xray_config_values[$key]}" "$file_to_substitute"
    done
}

function start_xray_warp_container_func () {
    docker compose -f $SCRIPT_DIR/docker-compose.yaml up -d
}

function main () {
    install_docker_tools
    create_docker_volume_caddyfile_func
    copy_config_from_template_file_func "templates/template.public.env" "./.public.env"
    copy_config_from_template_file_func "templates/caddyfile_test_template" "./config/caddy_config/Caddyfile"
    substitute_values_for_config_files_func "./.public.env"
    substitute_values_for_config_files_func "./config/caddy_config/Caddyfile"
    start_xray_warp_container_func
}

if [ "$#" -ne 6 ]; then
    echo "Error: Missing required parameters."
    echo "Usage: $0 <DOMAIN_NAME> <XRAY_PATH> <XRAY_UUID> <CLOUDFLARE_AUTH_TOKEN> <XRAY_ENCRYPTION_KEY> <XRAY_DECRYPTION_KEY>"
    exit 1
else
    main
fi