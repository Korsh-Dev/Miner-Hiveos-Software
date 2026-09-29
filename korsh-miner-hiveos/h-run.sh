#!/usr/bin/env bash
# ============================================================
# HiveOS Custom Miner Runner: Korsh Miner (Yespower 1.0)
# ============================================================

CUSTOM_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$CUSTOM_DIR"
CUSTOM_NAME="$(basename "$CUSTOM_DIR")"

. "$CUSTOM_DIR/h-manifest.conf" 2>/dev/null

conf="${CUSTOM_CONFIG_FILENAME:-$CUSTOM_DIR/${CUSTOM_NAME}.conf}"
if [[ ! -f "$conf" ]]; then
    echo "[!] Config file not found. Generating default..."
    ./h-config.sh
fi

if [[ -f "$conf" ]]; then
    . "$conf"
else
    echo "[!] Fatal: Could not read configuration file: $conf"
    exit 1
fi

# Locate executable binary
BIN="./korsh-miner-linux-x86_64"
if [[ ! -x "$BIN" ]]; then
    if [[ -x "./korsh-miner" ]]; then
        BIN="./korsh-miner"
    else
        chmod +x "$BIN" ./korsh-miner 2>/dev/null || true
    fi
fi

if [[ ! -x "$BIN" ]]; then
    echo "[!] Fatal: Miner binary not found or not executable!"
    exit 1
fi

# Optimization: Auto-enable HugePages for Yespower algorithm
ncpus=$(nproc 2>/dev/null || echo 4)
pages=$(( ncpus + 8 ))
if [[ -w /proc/sys/vm/nr_hugepages ]]; then
    echo $pages > /proc/sys/vm/nr_hugepages 2>/dev/null || true
fi
if command -v sysctl >/dev/null 2>&1; then
    sysctl -w vm.nr_hugepages=$pages >/dev/null 2>&1 || true
fi

# Setup log directory and clean log on fresh start
log_dir="$(dirname "$CUSTOM_LOG_BASENAME")"
mkdir -p "$log_dir"
log_file="${CUSTOM_LOG_BASENAME}.log"
> "$log_file"

# Assemble command arguments
cmd=("$BIN" "--stratum" "$POOL" "--user" "$USER" "--pass" "$PASS")

# Append extra user options (e.g., --threads 8, --no-pin)
if [[ -n "$USER_CONFIG" ]]; then
    # shellcheck disable=SC2206
    cmd+=($USER_CONFIG)
fi

echo "============================================================"
echo "          KORSH [KSH] CPU MINER — HIVEOS WORKER             "
echo "============================================================"
echo "Coin:       Korsh (KSH)"
echo "Algorithm:  Yespower 1.0"
echo "Pool:       $POOL"
echo "Worker:     $USER"
echo "Command:    ${cmd[*]}"
echo "Log file:   $log_file"
echo "============================================================"

# Execute miner in screen session and duplicate output to log file
exec "${cmd[@]}" 2>&1 | tee -a "$log_file"
