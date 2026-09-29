#!/usr/bin/env bash
# ============================================================
# Setup 2MB Hugepages for Yespower PoW
# ============================================================
set -euo pipefail
THREADS="$(( $(nproc 2>/dev/null || echo 2) ))"
PAGES=$(( THREADS + 8 ))
SUDO=""; [ "$(id -u)" -eq 0 ] || SUDO="sudo"
$SUDO sysctl -w "vm.nr_hugepages=$PAGES"
echo "vm.nr_hugepages=$PAGES" | $SUDO tee /etc/sysctl.d/90-korsh-hugepages.conf >/dev/null 2>&1 || true
echo "[+] Hugepages enabled: $PAGES pages reserved."
