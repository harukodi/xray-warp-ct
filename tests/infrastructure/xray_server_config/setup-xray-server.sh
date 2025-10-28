#!/bin/bash
# This script is used to test the connectivity of the xray warp ct container
SCRIPT_DIR=$(dirname "$(readlink -f "$0")")
declare -A xray_config_values=(
    ["DOMAIN_NAME"]="$1" 
    ["XRAY_PATH"]="$2"
    ["XRAY_UUID"]="$3"
    ["CLOUDFLARE_AUTH_TOKEN"]="$4"
    ["TLS_CERT_BASE64"]="$5"
    ["TLS_KEY_BASE64"]="$6"
)

function create_docker_tls_volume_bind_and_bind_tls_cert_and_key_func () {
    local CERT_DIR="${SCRIPT_DIR}/config/certs/caddy/certificates/acme-v02.api.letsencrypt.org-directory/${DOMAIN_NAME}"
    mkdir -p "$CERT_DIR"
    echo "$TLS_CERT_BASE64" | base64 -d > "${CERT_DIR}/${DOMAIN_NAME}.crt"
    echo "$TLS_KEY_BASE64" | base64 -d > "${CERT_DIR}/${DOMAIN_NAME}.key"
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

function copy_config_from_template_func () {
    cp $SCRIPT_DIR/template.public.env $SCRIPT_DIR/.public.env
}

function substitute_values_for_xray_client_config_helper_func () {
    local local_key="$1"
    local local_value="$2"
    sed -i "s/\${$local_key}/$local_value/g" $SCRIPT_DIR/.public.env
}

function substitute_values_for_xray_env_file_func () {
    for key in "${!xray_config_values[@]}"
    do
        substitute_values_for_xray_client_config_helper_func "$key" "${xray_config_values[$key]}"
    done
}

function start_xray_warp_container_func () {
    docker compose -f $SCRIPT_DIR/docker-compose.yaml up -d
}

function main () {
    install_docker_tools
    create_docker_tls_volume_bind_and_bind_tls_cert_and_key_func
    copy_config_from_template_func
    substitute_values_for_xray_env_file_func
    start_xray_warp_container_func
}

if [ "$#" -ne 6 ]; then
    echo "Error: Missing required parameters."
    echo "Usage: $0 <DOMAIN_NAME> <XRAY_PATH> <XRAY_UUID> <CLOUDFLARE_AUTH_TOKEN> <TLS_CERT_BASE64> <TLS_KEY_BASE64>"
    exit 1
else
    main
fi