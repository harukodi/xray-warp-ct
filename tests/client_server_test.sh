#!/bin/bash
SCRIPT_DIR=$(dirname "$(readlink -f "$0")")
declare -A xray_config_values=(
    ["HOST"]="$XRAY_HOST" 
    ["PATH"]="$XRAY_PATH"
    ["UUID"]="$XRAY_UUID"
)

function install_deps_packages_func () {
    echo "Installing needed deps packages..."
    sudo apt-get update
    sudo apt-get install curl wget jq net-tools -y
    echo "Deps packages installed"
}

function fetch_latest_xray_binary_func () {
    echo "Fetching latest Xray binary..."
    local latest_xray_tag=$(curl -s https://api.github.com/repos/XTLS/Xray-core/releases | jq -r '[.[] | select(.prerelease == false)][0].tag_name')
    echo "Latest Xray tag: $latest_xray_tag"
    
    local xray_binary_tmp_path="/tmp"
    local xray_binary_path="/usr/bin"
    sudo wget -O "$xray_binary_tmp_path/xray.zip" "https://github.com/XTLS/Xray-core/releases/download/$latest_xray_tag/Xray-linux-64.zip"
    sudo unzip -o "$xray_binary_tmp_path/xray.zip" -d "$xray_binary_tmp_path/xray"
    sudo mv "$xray_binary_tmp_path/xray/xray" "$xray_binary_path/xray"
    sudo chmod +x "$xray_binary_path/xray"
    echo "Xray binary installed: $(xray version)"
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
    echo "Configuration applied to client_config.json"
}

function test_xray_server_connectivity_func () {
    local COUNT=$1
    local XRAY_CONFIG_FILE="$SCRIPT_DIR/client_config.json"
    
    echo "Starting Xray with config: $XRAY_CONFIG_FILE"
    
    # Start Xray in background with logging
    xray run -c "$XRAY_CONFIG_FILE" > /tmp/xray.log 2>&1 &
    local XRAY_PID=$!
    
    echo "Xray started with PID: $XRAY_PID"
    
    # Wait for Xray to initialize
    sleep 8
    
    # Check if Xray process is running
    if ! ps -p $XRAY_PID > /dev/null; then
        echo "❌ Xray process died immediately"
        echo "Xray logs:"
        cat /tmp/xray.log
        return 1
    fi
    
    # Check if Xray is listening on the port
    echo "Checking listening ports:"
    netstat -tuln | grep -E ':(10809|10808)' || echo "No Xray ports found"
    
    for i in $(seq 1 $COUNT); do
        echo "=== Test attempt $i ==="
        
        # Test direct connectivity first (without proxy)
        echo "Testing direct connectivity..."
        local DIRECT_RESPONSE=$(curl -w "%{http_code}" -o /dev/null -s --connect-timeout 5 https://www.google.com)
        echo "Direct connection response: $DIRECT_RESPONSE"
        
        # Test SOCKS5 proxy
        echo "Testing SOCKS5 proxy..."
        local SOCKS_RESPONSE=$(curl -w "%{http_code}" -o /dev/null -s --connect-timeout 10 --socks5-hostname 127.0.0.1:10809 -L https://www.google.com)
        echo "SOCKS5 proxy response: $SOCKS_RESPONSE"
        
        # Test with verbose output for debugging
        if [[ "$SOCKS_RESPONSE" == "000" ]]; then
            echo "Debug SOCKS5 connection:"
            timeout 10 curl -v --socks5-hostname 127.0.0.1:10809 https://httpbin.org/ip 2>&1 | head -10
        fi
        
        if [[ "$SOCKS_RESPONSE" =~ [2-3][0-9][0-9] ]]; then
            echo "✅ SOCKS5 proxy test successful, status: $SOCKS_RESPONSE"
            kill $XRAY_PID
            wait $XRAY_PID 2>/dev/null
            return 0
        else
            echo "⚠️ SOCKS5 proxy test failed, status: $SOCKS_RESPONSE"
        fi
        
        sleep 10
    done
    
    echo "❌ All connection attempts failed"
    echo "Xray logs:"
    cat /tmp/xray.log
    kill $XRAY_PID 2>/dev/null
    return 1
}

function main () {
    local TRIES_COUNT=${1:-3}
    
    # Validate environment variables
    for var in XRAY_HOST XRAY_PATH XRAY_UUID; do
        if [[ -z "${!var}" ]]; then
            echo "❌ Missing environment variable: $var"
            exit 1
        fi
    done
    
    echo "Testing Xray server connectivity with $TRIES_COUNT attempts..."
    echo "Target host: $XRAY_HOST"
    
    install_deps_packages_func
    fetch_latest_xray_binary_func
    copy_config_from_template_func
    substitute_values_for_xray_client_config_func
    
    if test_xray_server_connectivity_func $TRIES_COUNT; then
        echo "✅ Xray server connectivity test passed"
        exit 0
    else
        echo "❌ Xray server connectivity test failed"
        exit 1
    fi
}

main 3