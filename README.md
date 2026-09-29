# Korsh Miner [KSH] — HiveOS Custom Miner Integration

<p align="center">
  <img src="korsh-miner/logo.png" alt="Korsh Logo" width="120">
</p>

<p align="center">
  <strong>Official HiveOS Custom Miner Package for Korsh Core (KSH)</strong><br>
  <em>High-performance CPU mining powered by the Yespower 1.0 ASIC-resistant algorithm</em>
</p>

<p align="center">
  <a href="https://github.com/Korsh-Dev/Miner-Hiveos-Software/releases"><img src="https://img.shields.io/github/v/release/Korsh-Dev/Miner-Hiveos-Software?style=flat-square&color=00CC52" alt="Release"></a>
  <a href="https://pool.korsh.org/"><img src="https://img.shields.io/badge/Pool-pool.korsh.org-5CC8FF?style=flat-square" alt="Pool"></a>
  <a href="https://explorer.korsh.org/"><img src="https://img.shields.io/badge/Explorer-explorer.korsh.org-00CC52?style=flat-square" alt="Explorer"></a>
  <a href="https://t.me/korshcommunity"><img src="https://img.shields.io/badge/Telegram-Community-5CC8FF?style=flat-square" alt="Telegram"></a>
  <a href="https://discord.gg/6xbqUWCDwu"><img src="https://img.shields.io/badge/Discord-Official-BB86FC?style=flat-square" alt="Discord"></a>
  <img src="https://img.shields.io/badge/Algorithm-Yespower%201.0-FFB300?style=flat-square" alt="Algorithm">
</p>

---

## ⚡ Overview

This repository provides the official **Custom Miner integration for HiveOS** to mine **Korsh (KSH)** with full telemetry, remote management, and auto-tuning:

- **Full HiveOS Dashboard Telemetry**: Live Hashrate in **kH/s**, Accepted/Rejected shares, Uptime, and CPU temperatures.
- **Auto-Enabling 2MB HugePages**: Automatically allocates memory pages to boost Yespower hashing performance by 15-30%.
- **Zero-Dependency Static Binary**: Self-contained 64-bit Linux executable (`korsh-miner-linux-x86_64`) compatible with all HiveOS versions.
- **Live Screen Console**: Supports standard HiveOS `miner` command for real-time monitoring and debugging.

---

## 🚀 Quick Setup in HiveOS (Flight Sheet)

### 1. Create a New Flight Sheet
In your HiveOS Dashboard, navigate to **Flight Sheets** and configure:

* **Coin**: `KSH` *(or type `KSH` to create the ticker)*
* **Wallet**: Your Korsh wallet address *(starts with `S`, e.g., `SSJ4n8AFfGHqvE8LTTbVyykjRoNCAL9rte`)*
* **Pool**: **Configure in miner**
* **Miner**: **Custom**

### 2. Setup Miner Config
Click the **Setup Miner Config** button and enter:

| Setting | Recommended Value |
| :--- | :--- |
| **Miner name** | `korsh-miner` |
| **Installation URL** | `https://github.com/Korsh-Dev/Miner-Hiveos-Software/releases/download/v1.0.0/korsh-miner-hiveos-v1.0.0.tar.gz` |
| **Hash algorithm** | `yespower` |
| **Wallet and worker template** | `%WAL%.%WORKER_NAME%` |
| **Pool URL** | `stratum+tcp://pool.korsh.org:3333` |
| **Pass** | `x` |
| **Extra config arguments** | *(Optional)* `--threads %CPU_THREADS%` *(or leave empty for auto-detect)* |

> **Direct IP Pool Fallback**: If DNS resolution fails on your rig, you can use `stratum+tcp://195.26.244.209:3333` as the Pool URL.

3. Click **Apply Changes**, name the Flight Sheet, and deploy it to your worker(s) 🚀.

---

## 💻 Manual Installation via SSH (Terminal)

You can also install or update the miner manually on any HiveOS rig:

```bash
# 1. Download and install using HiveOS custom-get
/hive/miners/custom/custom-get https://github.com/Korsh-Dev/Miner-Hiveos-Software/releases/download/v1.0.0/korsh-miner-hiveos-v1.0.0.tar.gz -f

# 2. Or download and extract manually
cd /hive/miners/custom
wget https://github.com/Korsh-Dev/Miner-Hiveos-Software/releases/download/v1.0.0/korsh-miner-hiveos-v1.0.0.tar.gz -O korsh-miner.tar.gz
tar -zxf korsh-miner.tar.gz
chmod +x /hive/miners/custom/korsh-miner/*.sh /hive/miners/custom/korsh-miner/korsh-miner*
```

---

## 📊 Useful HiveOS Commands

Run these directly inside your HiveOS shell (SSH or Shellinabox):

* `miner` — Open the live interactive console to watch accepted shares.
* `miner log` — View recent log outputs.
* `miner restart` — Restart the mining process.
* `miner stop` — Stop the miner.

---

## 🌐 Official Links

* **Official Mining Pool**: [https://pool.korsh.org/](https://pool.korsh.org/)
* **Pool Stratum Server**: `stratum+tcp://pool.korsh.org:3333` *(Direct IP: `stratum+tcp://195.26.244.209:3333`)*
* **Block Explorer**: [https://explorer.korsh.org/](https://explorer.korsh.org/)
* **Official Website**: [https://korsh.xyz](https://korsh.xyz)
* **Telegram**: [https://t.me/korshcommunity](https://t.me/korshcommunity)
* **Discord**: [https://discord.gg/6xbqUWCDwu](https://discord.gg/6xbqUWCDwu)
