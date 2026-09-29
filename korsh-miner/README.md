# Korsh Miner [KSH] — Official HiveOS Custom Miner Integration

Official high-performance **Yespower 1.0** CPU mining package for **Korsh Core (KSH)**, fully integrated with **HiveOS** as a native Custom Miner.

---

## ⚡ Key Features

- **Native HiveOS Telemetry**: Live Hashrate (**kH/s**), Accepted/Rejected shares, Uptime, and CPU temperatures directly in your HiveOS Web Dashboard and mobile app.
- **Yespower 1.0 Engine**: Custom ASIC-resistant PoW algorithm engineered for Korsh Core.
- **Automatic 2MB HugePages**: Auto-reserves huge pages upon launch to maximize hashing throughput on modern CPUs (Ryzen, EPYC, Threadripper, Intel Core i7/i9/Xeon).
- **Statically Linked Binary**: Zero external library dependencies (`glibc`, `openssl`, or `curl` version conflicts are completely eliminated).
- **Interactive Screen Console**: Full support for HiveOS `miner` command to stream live stratum logs, difficulty updates, and share confirmations.

---

## 🚀 HiveOS Flight Sheet Configuration

### Step 1: Create a Flight Sheet
1. In your **HiveOS** web dashboard, navigate to **Flight Sheets** and click **Add Flight Sheet**.
2. Set the following primary fields:
   - **Coin**: `KSH` *(or create custom coin `KSH`)*
   - **Wallet**: Select your Korsh wallet address *(starts with `S`, e.g., `SSJ4n8AFfGHqvE8LTTbVyykjRoNCAL9rte`)*
   - **Pool**: Select **Configure in miner**
   - **Miner**: Select **Custom**

### Step 2: Configure the Custom Miner
Click the yellow button **Setup Miner Config** and fill in the required parameters:

| Parameter | Configuration Value |
| :--- | :--- |
| **Miner name** | `korsh-miner` |
| **Installation URL** | `https://github.com/Korsh-Dev/Miner-Hiveos-Software/releases/download/v1.0.0/korsh-miner-hiveos-v1.0.0.tar.gz` |
| **Hash algorithm** | `yespower` |
| **Wallet and worker template** | `%WAL%.%WORKER_NAME%` |
| **Pool URL** | `stratum+tcp://pool.korsh.org:3333` |
| **Pass** | `x` |
| **Extra config arguments** | *(Optional)* `--threads %CPU_THREADS%` *(or leave blank for auto-detection)* |

> **Direct IP Pool Fallback**: If DNS resolution fails on your rig, you can use `stratum+tcp://195.26.244.209:3333` as the Pool URL.

### Step 3: Apply and Launch
1. Click **Apply Changes**.
2. Enter a name for the Flight Sheet (e.g., `Korsh KSH CPU Mining`).
3. Click **Create Flight Sheet**.
4. Apply the Flight Sheet to your workers using the rocket icon 🚀.

---

## 💻 Manual Installation via SSH / Terminal (Alternative)

If you prefer installing the package directly on the rig without hosting the `.tar.gz` archive on a public server:

```bash
# 1. Access your rig terminal (SSH or Shellinabox)
cd /hive/miners/custom

# 2. Download or upload the package to the rig
wget https://github.com/Korsh-Dev/Miner-Hiveos-Software/releases/download/v1.0.0/korsh-miner-hiveos-v1.0.0.tar.gz -O korsh-miner.tar.gz

# 3. Unpack the custom miner
tar -zxf korsh-miner.tar.gz

# 4. Ensure execution permissions
chmod +x /hive/miners/custom/korsh-miner/*.sh /hive/miners/custom/korsh-miner/korsh-miner*

# 5. Launch the miner via Flight Sheet
```

---

## 📊 Live Monitoring & Commands

Once mining has started on your rig:

- **`miner`**: Attaches to the miner's screen session to view live hashrate, incoming stratum jobs, difficulty changes, and accepted shares. Press `Ctrl+A, D` to detach.
- **`miner log`**: Tails the latest lines of `/var/log/miner/custom/korsh-miner/korsh-miner.log`.
- **`miner restart`**: Restarts the custom miner process.
- **`miner stop`**: Gracefully terminates mining.

---

## 🌐 Official Korsh Resources

- **Official Mining Pool**: [https://pool.korsh.org/](https://pool.korsh.org/)
- **Pool Stratum Server**: `stratum+tcp://pool.korsh.org:3333` *(Direct IP: `stratum+tcp://195.26.244.209:3333`)*
- **Block Explorer**: [https://explorer.korsh.org/](https://explorer.korsh.org/)
- **Official Website**: [https://korsh.xyz](https://korsh.xyz)
- **Telegram Community**: [https://t.me/korshcommunity](https://t.me/korshcommunity)
- **Discord**: [https://discord.gg/6xbqUWCDwu](https://discord.gg/6xbqUWCDwu)
