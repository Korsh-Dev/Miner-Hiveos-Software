#!/usr/bin/env bash
# ============================================================
# HiveOS Custom Miner Config Generator: Korsh Miner
# ============================================================

set -e

CUSTOM_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
CUSTOM_NAME="$(basename "$CUSTOM_DIR")"

# If invoked directly from /hive/miners/custom, redirect to miner subdirectory
if [[ "$CUSTOM_NAME" == "custom" ]]; then
    if [[ -d "$CUSTOM_DIR/korsh-miner-hiveos" ]]; then
        CUSTOM_NAME="korsh-miner-hiveos"
        CUSTOM_DIR="$CUSTOM_DIR/korsh-miner-hiveos"
    elif [[ -d "$CUSTOM_DIR/korsh-miner" ]]; then
        CUSTOM_NAME="korsh-miner"
        CUSTOM_DIR="$CUSTOM_DIR/korsh-miner"
    fi
fi

if [[ -f "$CUSTOM_DIR/h-manifest.conf" ]]; then
    . "$CUSTOM_DIR/h-manifest.conf" 2>/dev/null
fi

conf="${CUSTOM_CONFIG_FILENAME:-$CUSTOM_DIR/${CUSTOM_NAME}.conf}"
mkdir -p "$(dirname "$conf")"

# 1. Pool URL - Sanitization for korsh-miner binary
pool="${CUSTOM_URL}"
if [[ -z "$pool" ]]; then
    pool="stratum+tcp://pool.korsh.org:3333"
fi

# Strip any existing protocol prefix (http://, stratum://, tcp://, etc.)
clean_host_port=$(echo "$pool" | sed -E 's#^[a-zA-Z0-9+]+://##')
pool="stratum+tcp://${clean_host_port}"

# 2. Wallet & Worker template
user="${CUSTOM_TEMPLATE}"
if [[ -z "$user" ]]; then
    user="SSJ4n8AFfGHqvE8LTTbVyykjRoNCAL9rte.worker1"
fi
# Ensure clean address.worker formatting (replace slash with dot)
user=$(echo "$user" | tr '/' '.')

# 3. Password
pass="${CUSTOM_PASS:-x}"

# 4. Algo
algo="${CUSTOM_ALGO:-yespower}"

# 5. User Config / Extra parameters
user_config="${CUSTOM_USER_CONFIG}"

# Write config file
cat <<EOF > "$conf"
POOL="$pool"
USER="$user"
PASS="$pass"
ALGO="$algo"
USER_CONFIG="$user_config"
EOF

echo "[+] Korsh Miner config saved to: $conf (Pool: $pool | User: $user)"
