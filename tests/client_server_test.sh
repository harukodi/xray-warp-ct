#!/bin/bash
# This script is used to test the connectivity of the xray warp ct container
SCRIPT_DIR=$(dirname "$(readlink -f "$0")")
declare -A xray_config_values=(
    ["HOST"]="$XRAY_HOST" 
    ["PATH"]="$XRAY_PATH"
    ["UUID"]="$XRAY_UUID"
)

function install_deps_packages_func () {
    echo "Installing needed deps packages..."
    sudo apt-get update 2>&1 >/dev/null
    sudo apt-get install curl wget jq -y 2>&1 >/dev/null
    echo "Deps packages installed"
}

function fetch_latest_xray_binary_func () {
    local latest_xray_tag=$(curl -s https://api.github.com/repos/XTLS/Xray-core/releases | jq -r '[.[] | select(.prerelease == false)][0].tag_name')
    local xray_binary_tmp_path="/tmp"
    local xray_binary_path="/usr/bin"
    sudo wget -q -O "$xray_binary_tmp_path/xray.zip" "https://github.com/XTLS/Xray-core/releases/download/$latest_xray_tag/Xray-linux-64.zip" 2>&1 >/dev/null
    sudo unzip -o "$xray_binary_tmp_path/xray.zip" -d "$xray_binary_tmp_path/xray" 2>&1 >/dev/null
    sudo mv "$xray_binary_tmp_path/xray/xray" "$xray_binary_path/xray"
    sudo chmod +x "$xray_binary_path/xray"
    echo "Xray binary installed"
}

function copy_config_from_template_func () {
    cp $SCRIPT_DIR/client_config_template.json $SCRIPT_DIR/client_config.json
}

function substitute_values_for_xray_client_config_helper_func () {
    local local_key="$1"
    local local_value="$2"
    sed -i "s/\${$local_key}/$local_value/g" $SCRIPT_DIR/client_config.json
}

function substitute_values_for_xray_client_config_func () {
    for key in "${!xray_config_values[@]}"
    do
        substitute_values_for_xray_client_config_helper_func "$key" "${xray_config_values[$key]}"
    done
}

function test_xray_server_connectivity_func () {
    local COUNT=$1
    local XRAY_CONFIG_FILE="$SCRIPT_DIR/client_config.json"
    exec xray run -c "$XRAY_CONFIG_FILE" 2>&1 >/dev/null &
    local XRAY_PID=$!
    for i in $(seq 1 $COUNT); do
        sleep 10
        local RESPONSE=$(curl -w "%{http_code}" -o /dev/null -s --socks5-hostname 127.0.0.1:10809 -L https://google.com)
        if [[ "$RESPONSE" != "000" ]]; then
            echo "✅ Request succeeded xray server was reachable, status: $RESPONSE"
            kill $XRAY_PID
            exit 0
        else
            echo "⚠️ Waiting for Xray server to come online, status: $RESPONSE"
        fi
    done
    kill $XRAY_PID
}

function main () {
    local TRIES_COUNT=$1
    install_deps_packages_func
    fetch_latest_xray_binary_func
    copy_config_from_template_func
    substitute_values_for_xray_client_config_func
    test_xray_server_connectivity_func $TRIES_COUNT
    echo "❌ Timeout reached: Xray server did not respond in time. Test failed."
    exit 1
}
main 2