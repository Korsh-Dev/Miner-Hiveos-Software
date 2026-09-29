# Korsh Miner [KSH] — Integración Oficial para HiveOS (Español)

Paquete oficial de integración para minar **Korsh Core (KSH)** con algoritmo **Yespower 1.0** directamente en **HiveOS** como Custom Miner.

---

## 🚀 Configuración de Hoja de Vuelo (Flight Sheet) en HiveOS

1. En el panel de **HiveOS**, ve a **Flight Sheets** y crea una nueva:
   - **Coin**: `KSH`
   - **Wallet**: Tu dirección Korsh (comienza con `S`)
   - **Pool**: **Configure in miner** *(Configurar en el minero)*
   - **Miner**: **Custom** *(Personalizado)*

2. En **Setup Miner Config**, completa los campos:

| Campo | Valor |
| :--- | :--- |
| **Miner name** | `korsh-miner` |
| **Installation URL** | `https://tu-servidor/korsh-miner-hiveos-v1.0.0.tar.gz` |
| **Hash algorithm** | `yespower` |
| **Wallet and worker template** | `%WAL%.%WORKER_NAME%` |
| **Pool URL** | `stratum+tcp://korsh.xyz:3333` |
| **Pass** | `x` |
| **Extra config arguments** | *(Opcional)* `--threads %CPU_THREADS%` |

3. Haz clic en **Apply Changes**, nombra la Flight Sheet y presiona **Create Flight Sheet**.

---

## 📊 Monitoreo

- Escribe `miner` en la consola SSH para ver la pantalla en vivo.
- El Hashrate y los shares se reflejarán automáticamente en el panel web y la app móvil de HiveOS.
