# NovaTrade Copier Pro 🚀

A high-speed, local MT4 & MT5 trade copier built with Python & MQL. It synchronizes trades locally via shared MetaTrader JSON memory without third-party cloud servers.

---

## ✨ Features
- **Ultra-Low Latency**: Near-zero latency local file sync.
- **Cross-Platform**: Supports MT4 to MT4, MT4 to MT5, and MT5 to MT5.
- **Risk Management**: Lot multiplier and fixed lot sizing.
- **Prefix / Suffix Mapping**: Automatic mapping across brokers with different symbol naming.
- **Multilingual UI**: Persian, English, and Arabic.
- **Order Modification**: Syncs Open, Modify (SL/TP/Pending Price), and Close.

---

## ⚠️ Important MetaTrader Setup / نکات مهم در متاتریدر
> **EN:** To ensure the Expert Advisors (`.ex4` / `.ex5`) are visible and running properly:
> 1. Enable **AutoTrading** (MT4) or **Algo Trading** (MT5) in the top toolbar (Green icon).
> 2. In expert properties, check **Allow Live Trading** and **Allow DLL imports** (if prompted).
> 3. Refresh Navigator or restart MetaTrader after copying files to `MQL4/Experts` or `MQL5/Experts`.

<div dir="rtl">

> **راهنمای فارسی:** جهت اجرای صحیح اکسپرت‌ها (`.ex4` و `.ex5`) در متاتریدر:
>
> ۱. حتماً دکمه **AutoTrading** (در MT4) یا **Algo Trading** (در MT5) را از نوار بالای متاتریدر فعال کنید (آیکون سبز شود).  
> ۲. در تنظیمات اکسپرت (تب Common) گزینه **Allow Live Trading** یا **Allow Algo Trading** فعال باشد.  
> ۳. پس از کپی فایل‌ها در پوشه Experts، در پنجره Navigator کلیک‌راست کرده و **Refresh** را بزنید تا اکسپرت‌ها نمایش داده شوند.  

</div>


---

## 🛠️ Installation & Run
1. Install Python 3.8+ (or download the pre-built `NovaTradeCopierPro.exe` from Releases).
2. Attach `Master_Copier` to your master terminal chart and `Slave_Copier` to your slave terminal chart.
3. Run the copier hub:
```bash
   cd python_hub
   python copier_hub.py
   
☕ Support / Donate
If this project helped you, feel free to support development:

BSC (BEP-20): 0xCA51d83ACc5DB493f4d427226a93F4C3F82dDB0c
📄 License
This project is licensed under the MIT License.