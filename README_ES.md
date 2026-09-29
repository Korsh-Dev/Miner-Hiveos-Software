# Korsh Miner [KSH] — Integración Oficial para HiveOS (Español)

Paquete oficial de integración para minar **Korsh Core (KSH)** con algoritmo **Yespower 1.0** directamente en **HiveOS** como Custom Miner.

---

## 🚀 Configuración en HiveOS (Flight Sheet)

1. En el panel de **HiveOS**, ve a **Flight Sheets** y crea una nueva:
   - **Coin**: `KSH`
   - **Wallet**: Tu dirección Korsh (comienza con `S`)
   - **Pool**: **Configure in miner** *(Configurar en el minero)*
   - **Miner**: **Custom** *(Personalizado)*

2. En **Setup Miner Config**, completa los campos:

| Campo | Valor |
| :--- | :--- |
| **Miner name** | `korsh-miner-hiveos` |
| **Installation URL** | `https://github.com/Korsh-Dev/Miner-Hiveos-Software/releases/download/v1.0.0/korsh-miner-hiveos-v1.0.0.tar.gz` |
| **Hash algorithm** | `yespower` |
| **Wallet and worker template** | `%WAL%.%WORKER_NAME%` |
| **Pool URL** | `stratum+tcp://pool.korsh.org:3333` |
| **Pass** | `x` |
| **Extra config arguments** | *(Opcional)* `--threads %CPU_THREADS%` |

3. Haz clic en **Apply Changes**, guarda la Flight Sheet y aplícala a tu rig.

---

## 🌐 Enlaces Oficiales

- **Pool de Minería**: [https://pool.korsh.org/](https://pool.korsh.org/)
- **Servidor Stratum**: `stratum+tcp://pool.korsh.org:3333`
- **Explorador de Bloques**: [https://explorer.korsh.org/](https://explorer.korsh.org/)
