# Korsh Miner [KSH] — Official HiveOS Integration

Official high-performance **Yespower 1.0** CPU mining package for **Korsh Core (KSH)**, engineered specifically for **HiveOS**.

---

## ⚡ HiveOS Integration Highlights

- **Native Dashboard Telemetry**: Real-time Hashrate (**kH/s**), Accepted/Rejected shares, Uptime, and CPU temperatures.
- **Yespower 1.0 PoW Engine**: Custom algorithm optimized for multi-core processors (Ryzen, EPYC, Threadripper, Intel Core & Xeon).
- **Automatic 2MB HugePages**: Automatically allocates memory pages on startup to maximize hashrate.
- **Zero-Dependency Static Binary**: Self-contained 64-bit Linux executable (`korsh-miner-linux-x86_64`).
- **Standard Screen Console**: Full support for HiveOS `miner` command.

---

## 🚀 HiveOS Flight Sheet Configuration

### Step 1: Create or Edit a Flight Sheet
In your **HiveOS** dashboard, navigate to **Flight Sheets** -> **Add Flight Sheet**:
- **Coin**: `KSH`
- **Wallet**: Your Korsh wallet address *(starts with `S`, e.g., `SSJ4n8AFfGHqvE8LTTbVyykjRoNCAL9rte`)*
- **Pool**: **Configure in miner**
- **Miner**: **Custom**

### Step 2: Setup Miner Config
Click **Setup Miner Config** and fill in:

| Setting | Value |
| :--- | :--- |
| **Miner name** | `korsh-miner-hiveos` |
| **Installation URL** | `https://github.com/Korsh-Dev/Miner-Hiveos-Software/releases/download/v1.0.2/korsh-miner-hiveos-v1.0.2.tar.gz` |
| **Hash algorithm** | `yespower` |
| **Wallet and worker template** | `%WAL%.%WORKER_NAME%` |
| **Pool URL** | `stratum+tcp://pool.korsh.org:3333` |
| **Pass** | `x` |
| **Extra config arguments** | *(Optional)* `--threads %CPU_THREADS%` *(or leave blank for auto-detect)* |
| **Version** | *(Leave blank / empty)* |

> **Direct IP Fallback**: If DNS is slow on your rig, you can use `stratum+tcp://195.26.244.209:3333` as Pool URL.

### Step 3: Apply
Click **Apply Changes**, save the Flight Sheet, and deploy it to your worker with the **Rocket icon 🚀**.

---

## 💻 1-Step Installation & Fix via Terminal (Hive Shell / SSH)

To ensure a 100% clean install and bypass any package manager locks, run this single command in your rig's Hive Shell:

```bash
miner stop
mkdir -p /tmp/dummy-deb/DEBIAN
cat << 'EOF' > /tmp/dummy-deb/DEBIAN/control
Package: hive-miners-custom-1.0.2
Version: 1.0.2
Architecture: all
Maintainer: Korsh
Description: Korsh Custom Miner for HiveOS
EOF
dpkg-deb --build /tmp/dummy-deb /tmp/hive-miners-custom-1.0.2.deb 2>/dev/null
dpkg -i /tmp/hive-miners-custom-1.0.2.deb 2>/dev/null

/hive/miners/custom/custom-get https://github.com/Korsh-Dev/Miner-Hiveos-Software/releases/download/v1.0.2/korsh-miner-hiveos-v1.0.2.tar.gz -f

mkdir -p /hive/miners/custom/1.0.2
cp -rn /hive/miners/custom/korsh-miner-hiveos/* /hive/miners/custom/1.0.2/ 2>/dev/null || true

miner start
```

---

## 📊 HiveOS Commands

- **`miner`**: Attaches to the interactive screen session to view live hashrate, stratum jobs, and accepted shares.
  - **Detach/Exit**: Press **`Ctrl + A`**, then press **`D`** to exit the screen without stopping mining. *(Do NOT press `Ctrl + C`).*
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
