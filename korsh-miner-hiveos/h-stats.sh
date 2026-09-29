#!/usr/bin/env bash
# ============================================================
# HiveOS Custom Miner Stats Reporter: Korsh Miner
# ============================================================

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

log_basename="${CUSTOM_LOG_BASENAME:-/var/log/miner/custom/${CUSTOM_NAME}/${CUSTOM_NAME}}"
log_file="${log_basename}.log"
if [[ ! -f "$log_file" && -f "$CUSTOM_DIR/${CUSTOM_NAME}.log" ]]; then
    log_file="$CUSTOM_DIR/${CUSTOM_NAME}.log"
fi

khs=0
stats='{"hs":[0],"hs_units":"khs","temp":[],"fan":[],"uptime":0,"ar":[0,0],"algo":"yespower"}'

if [[ -f "$log_file" ]]; then
    if command -v python3 >/dev/null 2>&1; then
        eval "$(python3 -c '
import os, sys, time, json, re, subprocess

log_path = sys.argv[1]
algo = sys.argv[2] if len(sys.argv) > 2 else "yespower"

khs = 0.0
acc = 0
rej = 0
uptime = 0

# Get process uptime
try:
    pids = [int(p) for p in subprocess.check_output(["pgrep", "-f", "korsh-miner"], stderr=subprocess.DEVNULL).split()]
    if pids:
        pid = pids[0]
        out = subprocess.check_output(["ps", "-o", "etimes=", "-p", str(pid)], stderr=subprocess.DEVNULL).decode().strip()
        uptime = int(out.split()[0])
except Exception:
    if os.path.exists(log_path):
        uptime = int(max(0, time.time() - os.path.getctime(log_path)))

# Parse latest hashrate and shares from log
try:
    if os.path.exists(log_path):
        with open(log_path, "r", encoding="utf-8", errors="ignore") as f:
            lines = f.readlines()[-80:]
        
        for line in reversed(lines):
            m = re.search(r"rate=([\d\.]+)\s*(k?H/s)\s*shares:\s*submitted=\d+\s*accepted=(\d+)\s*rejected=(\d+)", line)
            if m:
                val = float(m.group(1))
                unit = m.group(2)
                acc = int(m.group(3))
                rej = int(m.group(4))
                khs = val if unit == "kH/s" else val / 1000.0
                break
except Exception:
    pass

# Retrieve CPU temperature (HiveOS cpu-temp tool or thermal zones)
temp = []
try:
    t_out = subprocess.check_output(["cpu-temp"], stderr=subprocess.DEVNULL, timeout=2).decode().strip()
    t_val = int(float(t_out.split()[0]))
    if 0 < t_val < 125:
        temp.append(t_val)
except Exception:
    pass

if not temp:
    for z in ["/sys/class/thermal/thermal_zone0/temp", "/sys/class/thermal/thermal_zone1/temp"]:
        if os.path.exists(z):
            try:
                with open(z) as f:
                    v = int(f.read().strip()) // 1000
                    if 0 < v < 125:
                        temp.append(v)
                        break
            except Exception:
                pass

stats_dict = {
    "hs": [round(khs, 3)],
    "hs_units": "khs",
    "temp": temp,
    "fan": [],
    "uptime": uptime,
    "ar": [acc, rej],
    "algo": algo
}

print(f"khs={round(khs, 3)}")
print(f"stats=\x27{json.dumps(stats_dict)}\x27")
' "$log_file" "yespower" 2>/dev/null)"
    else
        last_stat=$(grep -E 'rate=[0-9.]+' "$log_file" | tail -n 1)
        if [[ -n "$last_stat" ]]; then
            khs_val=$(echo "$last_stat" | sed -n 's/.*rate=\([0-9.]*\).*/\1/p')
            is_hs=$(echo "$last_stat" | grep -q ' H/s' && echo 1 || echo 0)
            if [[ "$is_hs" -eq 1 ]]; then
                khs=$(awk "BEGIN {print $khs_val / 1000.0}")
            else
                khs=$khs_val
            fi
            acc=$(echo "$last_stat" | sed -n 's/.*accepted=\([0-9]*\).*/\1/p')
            rej=$(echo "$last_stat" | sed -n 's/.*rejected=\([0-9]*\).*/\1/p')
            acc=${acc:-0}
            rej=${rej:-0}
            stats="{\"hs\":[$khs],\"hs_units\":\"khs\",\"temp\":[],\"fan\":[],\"uptime\":0,\"ar\":[$acc,$rej],\"algo\":\"yespower\"}"
        fi
    fi
fi

echo "khs=$khs"
echo "stats=$stats"
