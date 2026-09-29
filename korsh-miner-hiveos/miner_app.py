#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Korsh Miner App & Dashboard Server (Windows & Linux)
Monitors and controls the Yespower CPU miner and Korsh Core wallet
with visual web dashboard (http://localhost:8283), Stratum Pool and Solo Mining support.
"""

import os
import sys
import time
import json
import base64
import urllib.request
import urllib.error
import subprocess
import threading
import webbrowser
from http.server import HTTPServer, BaseHTTPRequestHandler
try:
    from http.server import ThreadingHTTPServer
except ImportError:
    ThreadingHTTPServer = HTTPServer
from datetime import datetime

PORT = 8283
if getattr(sys, 'frozen', False):
    BASE_DIR = os.path.dirname(os.path.abspath(sys.executable))
else:
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))

PARENT_DIR = os.path.abspath(os.path.join(BASE_DIR, ".."))

# Locate dashboard.html
HTML_FILE = os.path.join(BASE_DIR, "dashboard.html")
if not os.path.exists(HTML_FILE):
    HTML_FILE = os.path.join(BASE_DIR, "Korsh Miner", "dashboard.html")
if not os.path.exists(HTML_FILE):
    HTML_FILE = os.path.join(PARENT_DIR, "Korsh Miner", "dashboard.html")

# Locate miner_config.json
CONFIG_FILE = os.path.join(BASE_DIR, "miner_config.json")
if not os.path.exists(CONFIG_FILE) and os.path.exists(os.path.join(BASE_DIR, "Korsh Miner", "miner_config.json")):
    CONFIG_FILE = os.path.join(BASE_DIR, "Korsh Miner", "miner_config.json")
elif not os.path.exists(CONFIG_FILE) and os.path.exists(os.path.join(PARENT_DIR, "Korsh Miner", "miner_config.json")):
    CONFIG_FILE = os.path.join(PARENT_DIR, "Korsh Miner", "miner_config.json")

# Platform Detection
IS_WINDOWS = sys.platform.startswith("win")
IS_LINUX = sys.platform.startswith("linux") or sys.platform.startswith("darwin")

# Detect CPU Cores
DETECTED_CPUS = os.cpu_count() or 8
DEFAULT_THREADS = max(1, min(DETECTED_CPUS - 1 if DETECTED_CPUS > 2 else DETECTED_CPUS, 128))

# Detect Korsh DataDir (Windows & Linux)
if IS_WINDOWS:
    APPDATA = os.environ.get("APPDATA", "")
    DATADIR = os.path.join(APPDATA, "KorshCore")
    if not os.path.exists(os.path.join(DATADIR, "blocks")):
        fallback = os.path.join(APPDATA, "Korsh")
        if os.path.exists(os.path.join(fallback, "blocks")):
            DATADIR = fallback
else:
    HOME = os.path.expanduser("~")
    DATADIR = os.path.join(HOME, ".korshcore")
    if not os.path.exists(os.path.join(DATADIR, "blocks")):
        fallback = os.path.join(HOME, ".korsh")
        if os.path.exists(os.path.join(fallback, "blocks")):
            DATADIR = fallback

CONF_FILE = os.path.join(DATADIR, "korsh.conf")

# Default mining address
DEFAULT_ADDR = "SSJ4n8AFfGHqvE8LTTbVyykjRoNCAL9rte"

# Miner binary discovery
def find_miner_binary():
    candidates = []
    if IS_WINDOWS:
        candidates = [
            os.path.join(BASE_DIR, "korsh-miner.exe"),
            os.path.join(BASE_DIR, "Korsh Miner", "korsh-miner.exe"),
            os.path.join(PARENT_DIR, "Korsh Miner", "korsh-miner.exe"),
            os.path.join(PARENT_DIR, "korsh-miner.exe"),
            os.path.join(PARENT_DIR, "korsh-miner-windows-x86_64.exe"),
            os.path.join(BASE_DIR, "korsh-miner-windows-x86_64.exe"),
            os.path.join(BASE_DIR, "Korsh Miner", "korsh-miner-windows-x86_64.exe"),
        ]
    else:
        candidates = [
            os.path.join(BASE_DIR, "korsh-miner-linux-x86_64"),
            os.path.join(BASE_DIR, "Korsh Miner", "korsh-miner-linux-x86_64"),
            os.path.join(PARENT_DIR, "Korsh Miner", "korsh-miner-linux-x86_64"),
            os.path.join(PARENT_DIR, "korsh-miner-linux-x86_64"),
            os.path.join(BASE_DIR, "korsh-miner"),
            os.path.join(PARENT_DIR, "korsh-miner"),
        ]
    
    for c in candidates:
        if os.path.exists(c):
            if not IS_WINDOWS:
                try:
                    os.chmod(c, 0o755)
                except Exception:
                    pass
            return c
    return candidates[0] if candidates else "korsh-miner"

MINER_EXE = find_miner_binary()

# Default Configuration
DEFAULT_CONFIG = {
    "mode": "pool",
    "payout_address": DEFAULT_ADDR,
    "threads": DEFAULT_THREADS,
    "pool_url": "stratum+tcp://pool.korsh.org:3333",
    "worker_name": "worker1",
    "pool_pass": "x",
    "diff1": "scrypt"
}

def load_config():
    cfg = dict(DEFAULT_CONFIG)
    if os.path.exists(CONFIG_FILE):
        try:
            with open(CONFIG_FILE, "r", encoding="utf-8") as f:
                saved = json.load(f)
                cfg.update(saved)
        except Exception as e:
            print(f"[!] Error reading miner_config.json: {e}")
    return cfg

def save_config(new_cfg):
    try:
        with open(CONFIG_FILE, "w", encoding="utf-8") as f:
            json.dump(new_cfg, f, indent=2, ensure_ascii=False)
    except Exception as e:
        print(f"[!] Error saving miner_config.json: {e}")

config = load_config()

# Global state
state = {
    "system": {
        "os": "Windows" if IS_WINDOWS else ("Linux" if IS_LINUX else sys.platform),
        "cpu_count": DETECTED_CPUS,
        "is_windows": IS_WINDOWS,
        "is_linux": IS_LINUX,
        "binary": os.path.basename(MINER_EXE),
        "binary_path": MINER_EXE
    },
    "platform": {
        "os": "Windows" if IS_WINDOWS else ("Linux" if IS_LINUX else sys.platform),
        "detected_cpus": DETECTED_CPUS,
        "cpu_count": DETECTED_CPUS,
        "is_windows": IS_WINDOWS,
        "is_linux": IS_LINUX,
        "binary": os.path.basename(MINER_EXE)
    },
    "config": config,
    "node_online": False,
    "mining": {
        "is_mining": False,
        "mode": config.get("mode", "pool"),
        "threads": int(config.get("threads", DEFAULT_THREADS)),
        "payout_address": config.get("payout_address", DEFAULT_ADDR),
        "pool_url": config.get("pool_url", "stratum+tcp://pool.korsh.org:3333"),
        "worker_name": config.get("worker_name", "worker1"),
        "pool_pass": config.get("pool_pass", "x"),
        "hashrate": 0.0,
        "blocks_found": 0,
        "shares_accepted": 0,
        "shares_rejected": 0,
        "pool_diff": 0.0,
        "started_at": None,
    },
    "network": {
        "blocks": 0,
        "difficulty": 0.0,
        "networkhashps": 0.0,
        "connections": 0,
        "bestblockhash": "",
        "chain": "main"
    },
    "wallet": {
        "balance": 0.0,
        "address": config.get("payout_address", DEFAULT_ADDR)
    },
    "logs": []
}

# UTF-8 Console output safety for Windows
if sys.stdout and hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

logs_lock = threading.Lock()
worker_lock = threading.Lock()
worker_gen = 0
miner_process = None
miner_thread = None


def add_log(msg):
    ts = datetime.now().strftime("%H:%M:%S")
    line = f"[{ts}] {msg}"
    try:
        print(line)
    except Exception:
        try:
            print(line.encode("ascii", errors="replace").decode("ascii"))
        except Exception:
            pass
    with logs_lock:
        state["logs"].append(line)
        if len(state["logs"]) > 250:
            state["logs"].pop(0)


def get_rpc_auth():
    rpcuser = "korshminer"
    rpcpassword = "korshminingpass123"
    rpcport = "8282"
    if os.path.exists(CONF_FILE):
        try:
            with open(CONF_FILE, "r", encoding="utf-8", errors="ignore") as f:
                for line in f:
                    line = line.strip()
                    if line.startswith("rpcuser="):
                        rpcuser = line.split("=", 1)[1]
                    elif line.startswith("rpcpassword="):
                        rpcpassword = line.split("=", 1)[1]
                    elif line.startswith("rpcport="):
                        rpcport = line.split("=", 1)[1]
        except Exception:
            pass
    auth_header = "Basic " + base64.b64encode(f"{rpcuser}:{rpcpassword}".encode("ascii")).decode("ascii")
    url = f"http://127.0.0.1:{rpcport}"
    return url, auth_header


def rpc_call(method, params=[], wallet=None, timeout=5):
    base_url, auth_header = get_rpc_auth()
    url = f"{base_url}/wallet/{wallet}" if wallet else base_url
    payload = json.dumps({"jsonrpc": "1.0", "id": "miner_app", "method": method, "params": params}).encode("utf-8")
    req = urllib.request.Request(url, data=payload, headers={
        "Content-Type": "application/json",
        "Authorization": auth_header
    })
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            return data.get("result")
    except Exception:
        return None


def ensure_node_running():
    res = rpc_call("getmininginfo")
    if res is not None:
        state["node_online"] = True
        return True

    add_log("[NODE] Checking local Korsh node at 127.0.0.1:8282...")
    candidates = []
    if IS_WINDOWS:
        candidates = [
            r"C:\Users\lewis\Desktop\korsh-0.0.1-win64\korsh-0.0.1-win64\bin\korsh-qt.exe",
            os.path.join(BASE_DIR, "korsh-qt.exe"),
            os.path.join(PARENT_DIR, "korsh-0.0.1-win64", "bin", "korsh-qt.exe"),
        ]
    else:
        candidates = [
            "/usr/local/bin/korshd",
            "/usr/local/bin/korsh-qt",
            os.path.expanduser("~/korshd"),
            os.path.expanduser("~/korsh-qt")
        ]
    
    exe = None
    for c in candidates:
        if os.path.exists(c):
            exe = c
            break

    if exe:
        add_log(f"[NODE] Launching Korsh Core with RPC enabled ({exe})...")
        try:
            subprocess.Popen([exe, "-server=1"], cwd=os.path.dirname(exe))
            for _ in range(12):
                time.sleep(1.5)
                res = rpc_call("getmininginfo")
                if res is not None:
                    add_log("[NODE] Korsh Core node connected successfully!")
                    state["node_online"] = True
                    return True
        except Exception as e:
            add_log(f"[NODE] Could not launch local node automatically: {e}")
    else:
        add_log("[INFO] Solo mining requires Korsh Core running with -server=1. In Pool mode, a local node is not required.")
    return False


def solo_miner_worker(gen_id, threads, payout_addr):
    add_log("[SOLO] Starting SOLO mining engine via Korsh Core RPC (generatetoaddress)")
    add_log(f"[SOLO] Address: {payout_addr} | Threads: {threads}")

    mining_info = rpc_call("getmininginfo", timeout=5)
    if not mining_info:
        add_log("[NODE] Node not responding on port 8282. Checking local node...")
        if not ensure_node_running():
            add_log("[ERROR] Korsh Core node is not reachable on port 8282. Please start korsh-qt or korshd.")
            with worker_lock:
                if worker_gen == gen_id:
                    state["mining"]["is_mining"] = False
            return
        mining_info = rpc_call("getmininginfo", timeout=5)

    diff = float(mining_info.get("difficulty", 0.05)) if mining_info else 0.05
    blocks = mining_info.get("blocks", 0) if mining_info else 0
    add_log(f"[SOLO] Connected to Korsh Core RPC! Current Height: {blocks} | Difficulty: {diff:.5f}")

    with worker_lock:
        if worker_gen != gen_id:
            return
        state["mining"]["is_mining"] = True
        state["mining"]["started_at"] = time.time()
        state["mining"]["hashrate"] = 0.0
        state["mining"]["pool_diff"] = diff

    batch_size = 1500
    hashes_lock = threading.Lock()
    total_batch_hashes = 0
    start_time = time.time()
    last_log_time = time.time()
    last_hashes_count = 0

    def thread_task():
        nonlocal total_batch_hashes
        while True:
            with worker_lock:
                if worker_gen != gen_id:
                    break
            try:
                res = rpc_call("generatetoaddress", [1, payout_addr, batch_size], timeout=15)
                with hashes_lock:
                    total_batch_hashes += batch_size
                    if res and isinstance(res, list) and len(res) > 0:
                        for bhash in res:
                            state["mining"]["blocks_found"] += 1
                            add_log(f"[BLOCK FOUND] Block mined! Hash: {bhash} (+Reward sent to {payout_addr})")
            except Exception:
                time.sleep(0.5)

    sub_threads = []
    for _ in range(threads):
        t = threading.Thread(target=thread_task, daemon=True)
        t.start()
        sub_threads.append(t)

    try:
        while True:
            time.sleep(1.0)
            with worker_lock:
                if worker_gen != gen_id:
                    break

            now = time.time()
            with hashes_lock:
                current_total = total_batch_hashes

            elapsed = now - start_time
            if elapsed > 0:
                current_rate = current_total / elapsed
                with worker_lock:
                    if worker_gen == gen_id:
                        state["mining"]["hashrate"] = round(current_rate / 1000.0, 2)

            # Periodic log every 12 seconds
            if now - last_log_time >= 12.0:
                dt_window = now - last_log_time
                dh_window = current_total - last_hashes_count
                inst_rate = dh_window / dt_window if dt_window > 0 else 0
                add_log(f"rate={inst_rate:.0f} H/s ({inst_rate/1000.0:.2f} kH/s) blocks={state['mining']['blocks_found']} difficulty={diff:.5f}")
                last_log_time = now
                last_hashes_count = current_total
    finally:
        for t in sub_threads:
            t.join(timeout=1.0)
        with worker_lock:
            if worker_gen == gen_id:
                state["mining"]["is_mining"] = False
                state["mining"]["hashrate"] = 0.0
                add_log("[SYSTEM] Miner process stopped.")


def miner_worker(gen_id, mode, threads, payout_addr, pool_url, worker_name, pool_pass):
    global miner_process

    if mode == "solo":
        solo_miner_worker(gen_id, threads, payout_addr)
        return

    binary = find_miner_binary()
    if not os.path.exists(binary):
        add_log(f"[ERROR] Miner binary not found: {binary}")
        with worker_lock:
            if worker_gen == gen_id:
                state["mining"]["is_mining"] = False
        return

    # Build execution command
    user_param = f"{payout_addr}.{worker_name}" if worker_name else payout_addr
    cmd = [
        binary,
        "--stratum", pool_url,
        "--user", user_param,
        "--pass", pool_pass,
        "--threads", str(threads)
    ]
    add_log(f"[POOL] Starting POOL STRATUM mining: {pool_url}")
    add_log(f"[POOL] Worker: {user_param} | Threads: {threads}")

    try:
        proc = subprocess.Popen(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            bufsize=1,
            cwd=os.path.dirname(binary)
        )
        with worker_lock:
            if worker_gen != gen_id:
                # Cancelled before start
                try:
                    proc.kill()
                except Exception:
                    pass
                return
            miner_process = proc
            state["mining"]["is_mining"] = True
            state["mining"]["started_at"] = time.time()

        for line in iter(proc.stdout.readline, ''):
            line = line.strip()
            if not line:
                continue
            add_log(line)

            # Check if this generation is still active
            with worker_lock:
                if worker_gen != gen_id:
                    break

            # Parse Hashrate (e.g. rate=9209 H/s or rate=12.4 kH/s) and Shares
            if "rate=" in line:
                try:
                    after_rate = line.split("rate=")[1].strip()
                    parts = after_rate.split()
                    val = float(parts[0])
                    unit = parts[1].lower() if len(parts) > 1 else "h/s"
                    
                    if "mh/s" in unit:
                        state["mining"]["hashrate"] = round(val * 1000.0, 2)
                    elif "kh/s" in unit:
                        state["mining"]["hashrate"] = round(val, 2)
                    elif "h/s" in unit:
                        state["mining"]["hashrate"] = round(val / 1000.0, 2)
                    else:
                        state["mining"]["hashrate"] = round(val, 2)

                    if "blocks=" in line:
                        b = int(line.split("blocks=")[1].split()[0].strip())
                        state["mining"]["blocks_found"] = b
                    if "accepted=" in line:
                        acc = int(line.split("accepted=")[1].split()[0].strip())
                        old_acc = state["mining"]["shares_accepted"]
                        state["mining"]["shares_accepted"] = acc
                        if acc > old_acc:
                            diff_shares = acc - old_acc
                            add_log(f"[SHARE OK] {diff_shares} new share(s) accepted by pool! Total: {acc}")
                    if "rejected=" in line:
                        rej = int(line.split("rejected=")[1].split()[0].strip())
                        old_rej = state["mining"]["shares_rejected"]
                        state["mining"]["shares_rejected"] = rej
                        if rej > old_rej:
                            add_log(f"[SHARE REJECTED] Share rejected by pool! Total rejects: {rej}")
                except Exception:
                    pass
            elif "kH/s" in line and "diff" in line:
                try:
                    for part in line.split(","):
                        if "kH/s" in part:
                            state["mining"]["hashrate"] = float(part.replace("kH/s", "").strip())
                except Exception:
                    pass
            elif "yes!" in line.lower() or "share accepted" in line.lower():
                state["mining"]["shares_accepted"] += 1
                add_log(f"[SHARE OK] Share accepted by pool! Total: {state['mining']['shares_accepted']}")
            elif "block accepted" in line.lower() or "found block" in line.lower():
                state["mining"]["blocks_found"] += 1
                add_log("[BLOCK FOUND] Block accepted by the Korsh network! (+2 KSH)")

            # Parse Stratum Diff
            if "difficulty set to" in line:
                try:
                    diff_val = float(line.split("difficulty set to")[1].strip())
                    state["mining"]["pool_diff"] = diff_val
                except Exception:
                    pass
            elif "diff=" in line or "diff " in line:
                try:
                    tok = line.split("diff")[1].replace("=", " ").split()[0].strip()
                    state["mining"]["pool_diff"] = float(tok)
                except Exception:
                    pass

        proc.wait()
    except Exception as e:
        add_log(f"[ERROR] Miner execution error: {e}")
    finally:
        with worker_lock:
            # Only reset state if this worker is STILL the latest generation!
            if worker_gen == gen_id:
                state["mining"]["is_mining"] = False
                state["mining"]["hashrate"] = 0.0
                add_log("[SYSTEM] Miner process stopped.")


def stop_mining():
    global miner_process, worker_gen
    with worker_lock:
        worker_gen += 1
        proc = miner_process
        miner_process = None
        state["mining"]["is_mining"] = False
        state["mining"]["hashrate"] = 0.0

    if proc and proc.poll() is None:
        add_log("[SYSTEM] Stopping miner process...")
        try:
            proc.terminate()
            time.sleep(0.3)
            if proc.poll() is None:
                proc.kill()
        except Exception:
            pass
    else:
        add_log("[SYSTEM] Stopping miner process...")


def start_mining(mode=None, threads=None, addr=None, pool_url=None, worker=None, pool_pass=None):
    global miner_thread, worker_gen

    stop_mining()
    time.sleep(0.3)

    if mode:
        state["mining"]["mode"] = mode
    if threads:
        try:
            state["mining"]["threads"] = max(1, int(threads))
        except (ValueError, TypeError):
            pass
    if addr:
        state["mining"]["payout_address"] = addr
        state["wallet"]["address"] = addr
    if pool_url:
        state["mining"]["pool_url"] = pool_url
    if worker is not None:
        state["mining"]["worker_name"] = worker
    if pool_pass is not None:
        state["mining"]["pool_pass"] = pool_pass

    # Save to persistent config
    new_cfg = {
        "mode": state["mining"]["mode"],
        "threads": state["mining"]["threads"],
        "payout_address": state["mining"]["payout_address"],
        "pool_url": state["mining"]["pool_url"],
        "worker_name": state["mining"]["worker_name"],
        "pool_pass": state["mining"]["pool_pass"],
    }
    save_config(new_cfg)
    state["config"] = new_cfg

    # If solo mode, try ensuring node
    if state["mining"]["mode"] == "solo":
        ensure_node_running()

    with worker_lock:
        gen_id = worker_gen
        m = state["mining"]["mode"]
        t = state["mining"]["threads"]
        a = state["mining"]["payout_address"]
        p_url = state["mining"]["pool_url"]
        w = state["mining"]["worker_name"]
        p_pass = state["mining"]["pool_pass"]

    miner_thread = threading.Thread(
        target=miner_worker,
        args=(gen_id, m, t, a, p_url, w, p_pass),
        daemon=True
    )
    miner_thread.start()


def poll_node_loop():
    while True:
        try:
            info = rpc_call("getmininginfo")
            if info:
                state["node_online"] = True
                state["network"]["blocks"] = info.get("blocks", 0)
                state["network"]["difficulty"] = info.get("difficulty", 0.0)
                state["network"]["networkhashps"] = info.get("networkhashps", 0.0)
                state["network"]["chain"] = info.get("chain", "main")

                # Block hash
                bc = rpc_call("getblockchaininfo")
                if bc:
                    state["network"]["bestblockhash"] = bc.get("bestblockhash", "")

                # Connections
                net = rpc_call("getnetworkinfo")
                if net:
                    state["network"]["connections"] = net.get("connections", 0)

                # Wallet balance
                w = rpc_call("getwalletinfo", wallet="Dev")
                if w:
                    state["wallet"]["balance"] = w.get("balance", 0.0)
                else:
                    w_gen = rpc_call("getbalance")
                    if w_gen is not None:
                        state["wallet"]["balance"] = float(w_gen)
            else:
                state["node_online"] = False
        except Exception:
            state["node_online"] = False
        time.sleep(3.0)


class DashboardHandler(BaseHTTPRequestHandler):
    def serve_file(self, file_path, content_type):
        if os.path.exists(file_path):
            with open(file_path, "rb") as f:
                content = f.read()
            self.send_response(200)
            self.send_header("Content-Type", content_type)
            self.send_header("Content-Length", str(len(content)))
            if content_type.startswith("text/html"):
                self.send_header("Cache-Control", "no-cache, no-store, must-revalidate")
                self.send_header("Pragma", "no-cache")
                self.send_header("Expires", "0")
            else:
                self.send_header("Cache-Control", "public, max-age=3600")
            self.end_headers()
            self.wfile.write(content)
            return True
        return False

    def do_GET(self):
        clean_path = self.path.split("?")[0]
        if clean_path in ("/", "/index.html"):
            if not self.serve_file(HTML_FILE, "text/html; charset=utf-8"):
                self.send_response(404)
                self.end_headers()
                self.wfile.write(b"dashboard.html not found")
        elif clean_path == "/logo.png":
            p = os.path.join(BASE_DIR, "logo.png")
            if not os.path.exists(p):
                p = os.path.join(PARENT_DIR, "logo.png")
            if not self.serve_file(p, "image/png"):
                self.send_response(404)
                self.end_headers()
        elif clean_path == "/favicon.ico":
            p = os.path.join(BASE_DIR, "favicon.ico")
            if not os.path.exists(p):
                p = os.path.join(PARENT_DIR, "favicon.ico")
            if not self.serve_file(p, "image/x-icon"):
                self.send_response(404)
                self.end_headers()
        elif clean_path in ("/favicon.png", "/favicon-64x64.png"):
            fname = clean_path.lstrip("/")
            p = os.path.join(BASE_DIR, fname)
            if not os.path.exists(p):
                p = os.path.join(PARENT_DIR, fname)
            if not self.serve_file(p, "image/png"):
                self.send_response(404)
                self.end_headers()
        elif clean_path == "/api/status":
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.send_header("Access-Control-Allow-Origin", "*")
            self.end_headers()
            with logs_lock:
                data = json.dumps(state).encode("utf-8")
            self.wfile.write(data)
        else:
            self.send_response(404)
            self.end_headers()

    def do_POST(self):
        length = int(self.headers.get("Content-Length", 0))
        body = self.rfile.read(length).decode("utf-8") if length > 0 else "{}"
        try:
            params = json.loads(body)
        except Exception:
            params = {}

        clean_path = self.path.split("?")[0]
        if clean_path == "/api/start":
            mode = params.get("mode", state["mining"]["mode"])
            threads = params.get("threads", state["mining"]["threads"])
            addr = params.get("address", state["mining"]["payout_address"])
            pool_url = params.get("pool_url", state["mining"]["pool_url"])
            worker = params.get("worker", state["mining"]["worker_name"])
            pool_pass = params.get("pool_pass", state["mining"]["pool_pass"])
            start_mining(mode=mode, threads=threads, addr=addr, pool_url=pool_url, worker=worker, pool_pass=pool_pass)
        elif clean_path == "/api/stop":
            stop_mining()
        elif clean_path == "/api/save_config":
            for k in ["mode", "threads", "payout_address", "pool_url", "worker_name", "pool_pass"]:
                if k in params:
                    val = params[k]
                    if k == "threads":
                        val = max(1, int(val))
                    state["mining"][k] = val
            save_config(state["mining"])
            state["config"] = dict(state["mining"])
        elif clean_path == "/api/update_threads":
            t = params.get("threads")
            if t:
                try:
                    new_t = max(1, int(t))
                    state["mining"]["threads"] = new_t
                    state["config"]["threads"] = new_t
                    save_config(state["config"])
                    if state["mining"]["is_mining"]:
                        start_mining(threads=new_t)
                except (ValueError, TypeError):
                    pass

        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        with logs_lock:
            data = json.dumps(state).encode("utf-8")
        self.wfile.write(data)

    def log_message(self, format, *args):
        return


def get_lan_ip():
    try:
        import socket
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except Exception:
        return "127.0.0.1"


def main():
    print("=" * 64)
    print("      KORSH [KSH] CORE - MINING WORKSTATION & DASHBOARD")
    print("=" * 64)
    print(f"Operating System: {state['system']['os']}")
    print(f"Detected CPU Hardware: {DETECTED_CPUS} threads")
    print(f"Miner Binary: {MINER_EXE}")
    print(f"Data Directory: {DATADIR}")
    print(f"Initial Mode: {state['mining']['mode'].upper()} | Threads: {state['mining']['threads']}")
    print(f"Payout Address: {state['mining']['payout_address']}")
    print("=" * 64)

    # Background RPC poll for node stats
    poll_thread = threading.Thread(target=poll_node_loop, daemon=True)
    poll_thread.start()

    # Start local HTTP server (0.0.0.0 on Linux for HiveOS/LAN access, 127.0.0.1 on Windows)
    dash_host = os.environ.get("KORSH_HOST", "0.0.0.0" if IS_LINUX else "127.0.0.1")
    lan_ip = get_lan_ip()
    dash_url = f"http://localhost:{PORT}"
    lan_url = f"http://{lan_ip}:{PORT}" if lan_ip != "127.0.0.1" else None

    try:
        server = ThreadingHTTPServer((dash_host, PORT), DashboardHandler)
    except OSError as e:
        print(f"\n[!] Notice: Port {PORT} is already in use by an active Korsh Miner instance.")
        print(f"[+] Opening existing dashboard at: {dash_url}\n")
        try:
            webbrowser.open(dash_url)
        except Exception:
            pass
        print("Press any key or Ctrl+C to close this window.\n")
        try:
            time.sleep(3)
        except KeyboardInterrupt:
            pass
        return

    print(f"\n[+] Mining Dashboard active:")
    print(f"    - Local URL:   {dash_url}")
    if lan_url:
        print(f"    - Network URL: {lan_url} (Access from phones, rigs or other PCs)")
    print("[+] Opening browser automatically...\n")

    try:
        webbrowser.open(dash_url)
    except Exception:
        pass

    print("[i] Engine Status: STANDBY (Ready to configure and start from the Web Dashboard)")
    print("Press Ctrl+C in this console to stop the dashboard server and exit.\n")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nClosing Korsh Miner application...")
        stop_mining()
        server.server_close()
        sys.exit(0)


if __name__ == "__main__":
    main()
