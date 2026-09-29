# Korsh Miner [KSH] — HiveOS Custom Miner Integration

Official high-performance **Yespower 1.0** CPU mining package for **Korsh Core (KSH)**, engineered specifically for **HiveOS**.

---

## ⚡ HiveOS Integration Highlights

- **Native Dashboard Telemetry**: Real-time Hashrate (**kH/s**), Accepted/Rejected shares, Uptime, and CPU temperatures.
- **Yespower 1.0 Engine**: Custom PoW algorithm optimized for modern multi-core processors.
- **Automatic 2MB HugePages**: Automatically allocates memory pages to maximize throughput on Ryzen, EPYC, Threadripper, Intel Core & Xeon.
- **Zero-Dependency Static Binary**: Self-contained 64-bit Linux executable (`korsh-miner-linux-x86_64`).
- **Standard Screen Console**: Full support for HiveOS `miner` command.

---

## 🚀 HiveOS Flight Sheet Configuration

### Step 1: Create a Flight Sheet
In your **HiveOS** dashboard, go to **Flight Sheets** -> **Add Flight Sheet**:
- **Coin**: `KSH`
- **Wallet**: Your Korsh wallet address *(starts with `S`, e.g., `SSJ4n8AFfGHqvE8LTTbVyykjRoNCAL9rte`)*
- **Pool**: **Configure in miner**
- **Miner**: **Custom**

### Step 2: Setup Miner Config
Click **Setup Miner Config** and enter:

| Setting | Value |
| :--- | :--- |
| **Miner name** | `korsh-miner-hiveos` |
| **Installation URL** | `https://github.com/Korsh-Dev/Miner-Hiveos-Software/releases/download/v1.0.0/korsh-miner-hiveos-v1.0.0.tar.gz` |
| **Hash algorithm** | `yespower` |
| **Wallet and worker template** | `%WAL%.%WORKER_NAME%` |
| **Pool URL** | `stratum+tcp://pool.korsh.org:3333` |
| **Pass** | `x` |
| **Extra config arguments** | *(Optional)* `--threads %CPU_THREADS%` *(or leave blank for auto-detect)* |

> **Direct IP Fallback**: If DNS is slow on your rig, you can use `stratum+tcp://195.26.244.209:3333` as Pool URL.

### Step 3: Apply
Click **Apply Changes**, name the Flight Sheet, and deploy it to your worker 🚀.

---

## 💻 Manual Installation / Update via Terminal (SSH)

Run this command inside your HiveOS shell (SSH or Shellinabox):

```bash
/hive/miners/custom/custom-get https://github.com/Korsh-Dev/Miner-Hiveos-Software/releases/download/v1.0.0/korsh-miner-hiveos-v1.0.0.tar.gz -f
```

---

## 📊 HiveOS Commands

- **`miner`**: Attaches to the interactive screen session to view live hashrate, incoming stratum jobs, difficulty changes, and accepted shares. (`Ctrl+A, D` to detach).
- **`miner log`**: View recent miner logs.
- **`miner restart`**: Restart the miner.
- **`miner stop`**: Stop mining.

---

## 🌐 Official Korsh Resources

- **Mining Pool (Web)**: [https://pool.korsh.org/](https://pool.korsh.org/)
- **Pool Stratum Server**: `stratum+tcp://pool.korsh.org:3333` *(Direct IP: `stratum+tcp://195.26.244.209:3333`)*
- **Block Explorer**: [https://explorer.korsh.org/](https://explorer.korsh.org/)
- **Official Website**: [https://korsh.xyz](https://korsh.xyz)
- **Telegram**: [https://t.me/korshcommunity](https://t.me/korshcommunity)
- **Discord**: [https://discord.gg/6xbqUWCDwu](https://discord.gg/6xbqUWCDwu)
