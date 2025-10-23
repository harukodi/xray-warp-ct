#!/bin/bash
# This script is used to test the connectivity of the xray warp ct container
SCRIPT_DIR=$(dirname "$(readlink -f "$0")")
declare -A xray_config_values=(
    ["DOMAIN_NAME"]="$1" 
    ["XRAY_PATH"]="$2"
    ["XRAY_UUID"]="$3"
    ["CLOUDFLARE_AUTH_TOKEN"]="$4"
)

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
    docker-compose -f $SCRIPT_DIR/docker-compose.yaml up -d
}

function main () {
    copy_config_from_template_func
    substitute_values_for_xray_env_file_func
    start_xray_warp_container_func
}

if [ "$#" -ne 4 ]; then
    echo "Error: Missing required parameters."
    echo "Usage: $0 <DOMAIN_NAME> <XRAY_PATH> <XRAY_UUID> <CLOUDFLARE_AUTH_TOKEN>"
    exit 1
else
    main
fi