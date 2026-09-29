#!/usr/bin/env bash
# ============================================================
# HiveOS Custom Miner Config Generator: Korsh Miner
# ============================================================

set -e

# Source manifest if available
. /hive/miners/custom/korsh-miner/h-manifest.conf 2>/dev/null

conf="${CUSTOM_CONFIG_FILENAME:-/hive/miners/custom/korsh-miner/korsh-miner.conf}"
mkdir -p "$(dirname "$conf")"

# 1. Pool URL
pool="${CUSTOM_URL}"
if [[ -z "$pool" ]]; then
    pool="stratum+tcp://korsh.xyz:3333"
fi

# Ensure stratum+tcp:// prefix
if [[ "$pool" != stratum+tcp://* && "$pool" != stratum://* ]]; then
    pool="stratum+tcp://$pool"
fi

# 2. Wallet & Worker template
user="${CUSTOM_TEMPLATE}"
if [[ -z "$user" ]]; then
    user="SSJ4n8AFfGHqvE8LTTbVyykjRoNCAL9rte.worker1"
fi

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

echo "[+] Korsh Miner config saved to: $conf"
