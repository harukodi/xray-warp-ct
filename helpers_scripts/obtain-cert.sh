environment_variables=(
    CLOUDFLARE_DNS_API_TOKEN
    DOMAIN_NAME
    ACME_ACCOUNT
)

for var in "${environment_variables[@]}"; do
    if [[ -z "${!var}" ]]; then
        echo "❌ Missing environment variable: $var"
        exit 1
    fi
done

function install_lego_acme_client() {
    sudo snap install lego #>/dev/null 2>&1
}

function obtain_tls_cert () {
    sudo --preserve-env lego \
        --server=https://acme-staging-v02.api.letsencrypt.org/directory \
        --dns cloudflare \
        --domains="$DOMAIN_NAME" \
        --email="$ACME_ACCOUNT" \
        --accept-tos \
        run >/dev/null 2>&1

    if [[ $? -eq 0 ]];then
        echo "✅ Successfully obtained TLS certificate"
    else
        echo "❌ Failed to obtain TLS certificate"
        exit 1
    fi
}

function main() {
    install_lego_acme_client
    obtain_tls_cert
}

main