# Korsh Miner [KSH] — Integración Oficial para HiveOS (Español)

Paquete oficial de integración para minar **Korsh Core (KSH)** con algoritmo **Yespower 1.0** directamente en **HiveOS** como Custom Miner.

---

## 🚀 Configuración en HiveOS (Flight Sheet)

1. En el panel de **HiveOS**, ve a **Flight Sheets** y crea o edita la Flight Sheet:
   - **Coin**: `KSH`
   - **Wallet**: Tu dirección Korsh (comienza con `S`)
   - **Pool**: **Configure in miner**
   - **Miner**: **Custom**

2. En **Setup Miner Config**, completa los campos:

| Campo | Valor |
| :--- | :--- |
| **Miner name** | `korsh-miner-hiveos` |
| **Installation URL** | `https://github.com/Korsh-Dev/Miner-Hiveos-Software/releases/download/v1.0.2/korsh-miner-hiveos-v1.0.2.tar.gz` |
| **Hash algorithm** | `yespower` |
| **Wallet and worker template** | `%WAL%.%WORKER_NAME%` |
| **Pool URL** | `stratum+tcp://pool.korsh.org:3333` |
| **Pass** | `x` |
| **Extra config arguments** | *(Opcional)* `--threads %CPU_THREADS%` |
| **Version** | *(Dejar vacío / en blanco)* |

3. Haz clic en **Apply Changes**, guarda la Flight Sheet y aplícala a tu rig con el icono del **cohete 🚀**.

---

## 💻 Instalación y Solución en 1 Paso vía Terminal (Hive Shell / SSH)

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

## 📊 Ver Pantalla de Minería
Escribe en terminal:
```bash
miner
```
*(Para salir de la vista sin detener el minero, presiona **`Ctrl + A`** y luego **`D`**).*

---

## 🌐 Enlaces Oficiales

- **Pool de Minería**: [https://pool.korsh.org/](https://pool.korsh.org/)
- **Servidor Stratum**: `stratum+tcp://pool.korsh.org:3333`
- **Explorador de Bloques**: [https://explorer.korsh.org/](https://explorer.korsh.org/)
