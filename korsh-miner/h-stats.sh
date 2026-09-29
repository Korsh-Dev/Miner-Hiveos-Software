#!/usr/bin/env bash
# ============================================================
# HiveOS Custom Miner Stats Reporter: Korsh Miner
# ============================================================

. /hive/miners/custom/korsh-miner/h-manifest.conf 2>/dev/null

log_basename="${CUSTOM_LOG_BASENAME:-/var/log/miner/custom/korsh-miner/korsh-miner}"
log_file="${log_basename}.log"
if [[ ! -f "$log_file" && -f "/hive/miners/custom/korsh-miner/korsh-miner.log" ]]; then
    log_file="/hive/miners/custom/korsh-miner/korsh-miner.log"
fi

khs=0
stats='{"hs":[0],"hs_units":"khs","temp":[],"fan":[],"uptime":0,"ar":[0,0],"algo":"yespower"}'

if [[ -f "$log_file" ]]; then
    if command -v python3 >/dev/null 2>&1; then
        eval "$(python3 -c '
import os, sys, time, json, re

log_path = sys.argv[1]
algo = sys.argv[2] if len(sys.argv) > 2 else "yespower"

khs = 0.0
acc = 0
rej = 0
uptime = 0

try:
    if os.path.exists(log_path):
        ctime = os.path.getctime(log_path)
        uptime = int(max(0, time.time() - ctime))
        
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

temp = []
if os.path.exists("/sys/class/thermal/thermal_zone0/temp"):
    try:
        with open("/sys/class/thermal/thermal_zone0/temp") as f:
            t = int(f.read().strip()) // 1000
            if 0 < t < 120:
                temp.append(t)
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
print(f"stats='{json.dumps(stats_dict)}'")
' "$log_file" "yespower" 2>/dev/null)"
    else
        last_stat=$(grep -E 'rate=[0-9.]+' "$log_file" | tail -n 1)
        if [[ -n "$last_stat" ]]; then
            khs_val=$(echo "$last_stat" | sed -n 's/.*rate=\([0-9.]*\).*//p')
            is_hs=$(echo "$last_stat" | grep -q ' H/s' && echo 1 || echo 0)
            if [[ "$is_hs" -eq 1 ]]; then
                khs=$(awk "BEGIN {print $khs_val / 1000.0}")
            else
                khs=$khs_val
            fi
            acc=$(echo "$last_stat" | sed -n 's/.*accepted=\([0-9]*\).*//p')
            rej=$(echo "$last_stat" | sed -n 's/.*rejected=\([0-9]*\).*//p')
            acc=${acc:-0}
            rej=${rej:-0}
            stats="{"hs":[$khs],"hs_units":"khs","temp":[],"fan":[],"uptime":0,"ar":[$acc,$rej],"algo":"yespower"}"
        fi
    fi
fi

echo "khs=$khs"
echo "stats=$stats"
