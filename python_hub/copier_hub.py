# -*- coding: utf-8 -*-
"""
سیستم کپی‌ترید محلی حرفه‌ای - نسخه ۴.۱۰ پرو
Local Trade Copier Hub Pro - v4.10 (Dark Modern Edition)
اصلاحات: بهینه‌سازی فونت فارسی لاگ، آدرس ولت بایننس اسمارت چین (BEP-20)
"""

import os
import json
import time
import threading
import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
from datetime import datetime

# مسیر فایل‌های مشترک متاتریدر
APPDATA = os.getenv('APPDATA')
COMMON_FILES_DIR = os.path.join(APPDATA, r"MetaQuotes\Terminal\Common\Files")
os.makedirs(COMMON_FILES_DIR, exist_ok=True)

terminals_data = {}
app_config = {
    "master_id": "",
    "slave_id": "",
    "lot_mode": "Multiplier",
    "lot_value": 1.0,
    "master_prefix": "",
    "master_suffix": "",
    "slave_prefix": "",
    "slave_suffix": "",
    "lang": "fa"
}

# آدرس و شبکه کیف پول دونیت (Binance Smart Chain - BEP-20)
DONATE_WALLET_ADDRESS = "0xCA51d83ACc5DB493f4d427226a93F4C3F82dDB0c"
DONATE_NETWORK = "BEP-20 (BSC)"

# فرهنگ لغت سه زبانه
TRANSLATIONS = {
    "fa": {
        "title": "NovaTrade Copier Hub Pro | نسخه ۴.۱۰",
        "menu_file": "فایل",
        "menu_exit": "خروج از برنامه",
        "menu_lang": "زبان‌ها (Language)",
        "menu_help": "راهنما و پشتیبانی",
        "menu_about": "درباره نرم‌افزار",
        "menu_donate": "حمایت مالی (Donate)",
        "hero_title": "NOVATRADE COPIER PRO",
        "hero_sub": "هسته محلی و فوق‌سریع کپی‌ترید بین ترمینال‌های MT4 و MT5",
        "lang_lbl": "زبان محیط کاربری:",
        "frame_terminals": " ۱. پیکربندی ترمینال‌های معاملاتی ",
        "master_lbl": "ترمینال فرستنده (Master):",
        "slave_lbl": "ترمینال گیرنده (Slave):",
        "frame_lot": " ۲. تنظیمات مدیریت ریسک و حجم (Lot Sizing) ",
        "lot_mult": "ضریب حجم مستر (Multiplier)",
        "lot_fixed": "لات ثابت برای تمام معاملات (Fixed)",
        "lot_val": "مقدار اعمالی:",
        "frame_symbols": " ۳. هماهنگ‌سازی نماد و بروکرها (Prefix / Suffix) ",
        "m_pre": "پیشوند مستر:",
        "m_suf": "پسوند مستر:",
        "s_pre": "پیشوند اسلیو:",
        "s_suf": "پسوند اسلیو:",
        "btn_apply": "ذخیره و فعال‌سازی همگام‌سازی",
        "frame_donate": f" حمایت مالی از پروژه - شبکه بایننس اسمارت چین ({DONATE_NETWORK}) ",
        "btn_copy_wallet": "کپی آدرس ولت",
        "wallet_copied": f"آدرس ولت ({DONATE_NETWORK}) در کلیپ‌بورد کپی شد!\nبا تشکر از حمایت شما.",
        "frame_log": " ۴. مانیتورینگ زنده و لاگ تبادل دستورات ",
        "btn_clear_log": "پاکسازی لاگ",
        "ready": "هسته محلی پایتون آماده است. مسیر شنود:",
        "terminal_found": "ترمینال فعال متصل شد:",
        "applied": "همگام‌سازی فعال شد: مستر [{master}] به اسلیو [{slave}] متصل گردید.",
        "no_slave": "[هشدار] ترمینال اسلیو (گیرنده) انتخاب نشده است!",
        "cmd_sent": "[فرمان اسلیو] فایل: {file} | دستور: {act} | تیکت: {tkt}",
        "skip_initial": "[رد شد] معامله قبلی مستر همگام نشد: {tkt} ({type})",
        "new_order": "[سفارش جدید] نوع: {type} | نماد: {sym} | حجم: {lot} | تیکت: {tkt}",
        "mod_order": "[اصلاح سفارش] تیکت: {tkt} | حدضرر: {sl} | سود: {tp} | قیمت: {price}",
        "close_order": "[بسته شدن] تیکت مستر: {tkt} لغو/بسته شد. دستور بستن ارسال گردید.",
        "loop_err": "[خطای مانیتورینگ]:",
        "about_text": f"سیستم کپی‌ترید محلی بدون تأخیر\nنسخه: 4.10 Pro\nآدرس دونیت (BEP-20):\n{DONATE_WALLET_ADDRESS}"
    },
    "en": {
        "title": "NovaTrade Copier Hub Pro | v4.10",
        "menu_file": "File",
        "menu_exit": "Exit",
        "menu_lang": "Languages",
        "menu_help": "Help",
        "menu_about": "About",
        "menu_donate": "Donate",
        "hero_title": "NOVATRADE COPIER PRO",
        "hero_sub": "Ultra-Low Latency MT4/MT5 Local Trade Synchronizer",
        "lang_lbl": "Interface Language:",
        "frame_terminals": " 1. Trading Terminals Configuration ",
        "master_lbl": "Master Terminal (Sender):",
        "slave_lbl": "Slave Terminal (Receiver):",
        "frame_lot": " 2. Lot Sizing & Risk Management ",
        "lot_mult": "Lot Multiplier",
        "lot_fixed": "Fixed Lot Size",
        "lot_val": "Value:",
        "frame_symbols": " 3. Symbol Broker Mapping (Prefix/Suffix) ",
        "m_pre": "Master Prefix:",
        "m_suf": "Master Suffix:",
        "s_pre": "Slave Prefix:",
        "s_suf": "Slave Suffix:",
        "btn_apply": "Save & Activate Synchronizer",
        "frame_donate": f" Support Development - Binance Smart Chain ({DONATE_NETWORK}) ",
        "btn_copy_wallet": "Copy Address",
        "wallet_copied": f"Wallet Address ({DONATE_NETWORK}) copied to clipboard!\nThank you for your support.",
        "frame_log": " 4. Live Activity Stream & Command Log ",
        "btn_clear_log": "Clear Log",
        "ready": "Local Python Hub active. Monitored Path:",
        "terminal_found": "Live terminal attached:",
        "applied": "Sync Enabled: Master [{master}] connected to Slave [{slave}].",
        "no_slave": "[Warning] Slave terminal not selected!",
        "cmd_sent": "[Slave Command] File: {file} | Action: {act} | Ticket: {tkt}",
        "skip_initial": "[Ignored] Pre-existing Master Order skipped: {tkt} ({type})",
        "new_order": "[New Order] Type: {type} | Symbol: {sym} | Vol: {lot} | Ticket: {tkt}",
        "mod_order": "[Modified] Ticket: {tkt} | SL: {sl} | TP: {tp} | Price: {price}",
        "close_order": "[Closed] Master Ticket: {tkt} closed/cancelled. Close sent.",
        "loop_err": "[Watcher Loop Error]:",
        "about_text": f"Zero Latency Local Trade Copier\nVersion: 4.10 Pro\nDonate Address (BEP-20):\n{DONATE_WALLET_ADDRESS}"
    },
    "ar": {
        "title": "ناسخ الصفقات المحلي الإحترافي | v4.10",
        "menu_file": "ملف",
        "menu_exit": "خروج",
        "menu_lang": "اللغات (Language)",
        "menu_help": "مساعدة",
        "menu_about": "حول البرنامج",
        "menu_donate": "دعم المطور (Donate)",
        "hero_title": "NOVATRADE COPIER PRO",
        "hero_sub": "نواة النسخ الفوري بين منصات MT4 و MT5 بسرعة فائقة",
        "lang_lbl": "لغة البرنامج:",
        "frame_terminals": " ١. إعداد منصات التداول ",
        "master_lbl": "المنصة المصدر (Master):",
        "slave_lbl": "المنصة المستقبلة (Slave):",
        "frame_lot": " ٢. إدارة حجم الصفقات والمخاطر ",
        "lot_mult": "مضاعف اللوت (Multiplier)",
        "lot_fixed": "لوت ثابت لجميع الصفقات",
        "lot_val": "القيمة:",
        "frame_symbols": " ٣. مطابقة رموز أزواج العملات ",
        "m_pre": "بادئة المصدر:",
        "m_suf": "لاحقة المصدر:",
        "s_pre": "بادئة المستقبل:",
        "s_suf": "لاحقة المستقبل:",
        "btn_apply": "حفظ وتفعيل المزامنة المباشرة",
        "frame_donate": f" دعم تطوير البرنامج - شبكة بينانس الذكية ({DONATE_NETWORK}) ",
        "btn_copy_wallet": "نسخ عنوان المحفظة",
        "wallet_copied": f"تم نسخ عنوان المحفظة ({DONATE_NETWORK}) بنجاح!",
        "frame_log": " ٤. سجل الأحداث الفوري والمراقبة ",
        "btn_clear_log": "مسح السجل",
        "ready": "النظام المحلي جاهز. مسار المراقبة:",
        "terminal_found": "تم ربط المنصة:",
        "applied": "تم تفعيل النسخ: من [{master}] إلى [{slave}].",
        "no_slave": "[تحذير] لم يتم تحديد المنصة المستقبلة!",
        "cmd_sent": "[أمر المستقبل] ملف: {file} | الإجراء: {act} | التذكرة: {tkt}",
        "skip_initial": "[تم التجاهل] الصفقة السابقة للمصدر تم تجاهلها: {tkt} ({type})",
        "new_order": "[صفقة جديدة] نوع: {type} | الرمز: {sym} | اللوت: {lot} | تذكرة: {tkt}",
        "mod_order": "[تعديل أمر] تذكرة: {tkt} | SL: {sl} | TP: {tp} | السعر: {price}",
        "close_order": "[إغلاق صفقة] تذكرة المصدر: {tkt} تم إغلاقها.",
        "loop_err": "[خطأ في المراقبة]:",
        "about_text": f"ناسخ صفقات محلي فائق السرعة\nالإصدار: 4.10 Pro\nعنوان الدعم ({DONATE_NETWORK}):\n{DONATE_WALLET_ADDRESS}"
    }
}

tracked_master_orders = {}
initial_sync_done = False


def get_text(key):
    lang = app_config.get("lang", "fa")
    return TRANSLATIONS.get(lang, TRANSLATIONS["fa"]).get(key, key)


def log_event(text):
    now = datetime.now().strftime("%H:%M:%S")
    msg = f"[{now}] {text}\n"
    if 'root' in globals() and root and 'log_area' in globals() and log_area:
        root.after(0, lambda: _append_log(msg))
    else:
        print(msg, end="")


def _append_log(msg):
    log_area.insert(tk.END, msg)
    log_area.see(tk.END)


def read_json_flexible(fpath):
    for enc in ('latin-1', 'cp1256', 'utf-8', 'utf-16', 'utf-8-sig'):
        try:
            with open(fpath, "r", encoding=enc) as f:
                content = f.read().strip()
                if content:
                    return json.loads(content)
        except Exception:
            continue
    return None


def transform_symbol(master_sym):
    clean_sym = master_sym
    if app_config["master_prefix"] and clean_sym.startswith(app_config["master_prefix"]):
        clean_sym = clean_sym[len(app_config["master_prefix"]):]
    if app_config["master_suffix"] and clean_sym.endswith(app_config["master_suffix"]):
        clean_sym = clean_sym[:-len(app_config["master_suffix"])]
    return f"{app_config['slave_prefix']}{clean_sym}{app_config['slave_suffix']}"


def calculate_slave_lot(master_lot):
    if app_config["lot_mode"] == "Fixed":
        return round(float(app_config["lot_value"]), 2)
    return round(float(master_lot) * float(app_config["lot_value"]), 2)


def send_command_to_slave(cmd):
    slave_id = app_config["slave_id"]
    if not slave_id:
        log_event(get_text("no_slave"))
        return

    cmd_filename = f"cmd_{slave_id}.json"
    cmd_file = os.path.join(COMMON_FILES_DIR, cmd_filename)

    for _ in range(5):
        try:
            cmds = []
            if os.path.exists(cmd_file):
                try:
                    data = read_json_flexible(cmd_file)
                    if isinstance(data, list):
                        cmds = data
                except Exception:
                    pass

            cmds.append(cmd)
            raw_text = json.dumps(cmds, separators=(',', ':'), ensure_ascii=True)

            with open(cmd_file, "w", encoding="latin-1", newline='') as f:
                f.write(raw_text)

            log_event(get_text("cmd_sent").format(
                file=cmd_filename,
                act=cmd.get('action'),
                tkt=cmd.get('master_ticket')
            ))
            return
        except PermissionError:
            time.sleep(0.04)
        except Exception:
            time.sleep(0.04)


def process_master_orders(master_orders):
    global initial_sync_done
    current_master_map = {str(o.get("ticket")): o for o in master_orders if o.get("ticket")}

    # جلوگیری از کپی معاملات باز و پندینگ‌های پیش از شروع هاب
    if not initial_sync_done:
        for t_id, o in current_master_map.items():
            tracked_master_orders[t_id] = {
                "sl": round(float(o.get("sl", 0.0)), 5),
                "tp": round(float(o.get("tp", 0.0)), 5),
                "price": round(float(o.get("open_price", 0.0)), 5),
                "type": str(o.get("type", "")).upper()
            }
            log_event(get_text("skip_initial").format(tkt=t_id, type=o.get('type')))
        initial_sync_done = True
        return

    # بررسی سفارش‌های جدید یا اصلاح‌شده
    for t_id, ord_info in current_master_map.items():
        o_type = str(ord_info.get("type", "")).upper()
        sym = transform_symbol(ord_info.get("symbol", ""))
        lot = calculate_slave_lot(ord_info.get("volume", 0.01))
        open_price = round(float(ord_info.get("open_price", 0.0)), 5)
        cur_sl = round(float(ord_info.get("sl", 0.0)), 5)
        cur_tp = round(float(ord_info.get("tp", 0.0)), 5)

        if t_id not in tracked_master_orders:
            tracked_master_orders[t_id] = {
                "sl": cur_sl,
                "tp": cur_tp,
                "price": open_price,
                "type": o_type
            }
            cmd = {
                "action": "OPEN",
                "master_ticket": int(t_id),
                "type": o_type,
                "symbol": sym,
                "volume": lot,
                "price": open_price,
                "sl": cur_sl,
                "tp": cur_tp
            }
            log_event(get_text("new_order").format(type=o_type, sym=sym, lot=lot, tkt=t_id))
            send_command_to_slave(cmd)
        else:
            last_state = tracked_master_orders[t_id]
            sl_changed = abs(last_state["sl"] - cur_sl) > 0.00001
            tp_changed = abs(last_state["tp"] - cur_tp) > 0.00001
            price_changed = abs(last_state["price"] - open_price) > 0.00001
            is_pending = ("LIMIT" in o_type) or ("STOP" in o_type)

            if sl_changed or tp_changed or (price_changed and is_pending):
                tracked_master_orders[t_id]["sl"] = cur_sl
                tracked_master_orders[t_id]["tp"] = cur_tp
                tracked_master_orders[t_id]["price"] = open_price

                cmd = {
                    "action": "MODIFY",
                    "master_ticket": int(t_id),
                    "price": open_price,
                    "sl": cur_sl,
                    "tp": cur_tp
                }
                log_event(get_text("mod_order").format(tkt=t_id, sl=cur_sl, tp=cur_tp, price=open_price))
                send_command_to_slave(cmd)

    # بررسی و بستن سفارش‌های حذف شده
    for known_ticket in list(tracked_master_orders.keys()):
        if known_ticket not in current_master_map:
            cmd = {
                "action": "CLOSE",
                "master_ticket": int(known_ticket)
            }
            log_event(get_text("close_order").format(tkt=known_ticket))
            send_command_to_slave(cmd)
            del tracked_master_orders[known_ticket]


def file_watcher_loop():
    while True:
        try:
            files = os.listdir(COMMON_FILES_DIR)
            for fname in files:
                if fname.startswith("status_") and fname.endswith(".json"):
                    fpath = os.path.join(COMMON_FILES_DIR, fname)
                    data = read_json_flexible(fpath)
                    if data and isinstance(data, dict):
                        term_id = data.get("terminal_id")
                        if term_id:
                            is_new = term_id not in terminals_data
                            terminals_data[term_id] = {
                                "platform": data.get("platform"),
                                "account": data.get("account"),
                                "orders": data.get("orders", []),
                                "last_seen": datetime.now().strftime("%H:%M:%S")
                            }
                            if is_new:
                                log_event(f"{get_text('terminal_found')} {term_id} ({data.get('platform')})")

                            if term_id == app_config["master_id"] and app_config["slave_id"]:
                                process_master_orders(data.get("orders", []))
        except Exception as e:
            log_event(f"{get_text('loop_err')} {e}")
        time.sleep(0.08)


class CopierGUI:
    def __init__(self, root):
        self.root = root
        self.root.geometry("890x800")
        self.root.minsize(840, 740)
        self.root.configure(bg="#0c1017")

        self._setup_styles()
        self._build_menu()
        self._build_ui()
        self.apply_language_texts()
        self.update_terminals_list()

    def _setup_styles(self):
        style = ttk.Style()
        style.theme_use("clam")

        BG_COLOR = "#0c1017"
        FRAME_BG = "#131b26"
        ACCENT_CYAN = "#00d2ff"
        TEXT_LIGHT = "#e6edf3"

        style.configure(".", background=BG_COLOR, foreground=TEXT_LIGHT, font=("Segoe UI", 9))

        style.configure("TLabelframe", background=FRAME_BG, relief="solid", borderwidth=1)
        style.configure("TLabelframe.Label", background=FRAME_BG, foreground=ACCENT_CYAN, font=("Segoe UI", 10, "bold"))

        style.configure("TLabel", background=FRAME_BG, foreground=TEXT_LIGHT, font=("Segoe UI", 9))
        style.configure("Header.TLabel", background="#131b26", foreground="#ffffff")
        style.configure("SubHeader.TLabel", background="#131b26", foreground="#7d8b99")

        style.configure("TRadiobutton", background=FRAME_BG, foreground=TEXT_LIGHT, font=("Segoe UI", 9))

        # استایل دکمه ذخیره اصلی
        style.configure("Primary.TButton", background="#00e676", foreground="#000000", font=("Segoe UI", 10, "bold"),
                        borderwidth=0)
        style.map("Primary.TButton", background=[("active", "#00c853")])

        # استایل دکمه کپی دونیت
        style.configure("Donate.TButton", background="#ffb300", foreground="#000000", font=("Segoe UI", 9, "bold"))
        style.map("Donate.TButton", background=[("active", "#ffa000")])

        style.configure("Secondary.TButton", background="#21262d", foreground="#c9d1d9", font=("Segoe UI", 8))
        style.map("Secondary.TButton", background=[("active", "#30363d")])

        style.configure("TCombobox", fieldbackground="#1b2432", background="#21262d", foreground="#ffffff",
                        arrowcolor="#00d2ff")
        style.configure("TEntry", fieldbackground="#1b2432", foreground="#ffffff")

    def _build_menu(self):
        menubar = tk.Menu(self.root, bg="#161b22", fg="#ffffff", activebackground="#00d2ff", activeforeground="#000000",
                          borderwidth=0)

        self.menu_file = tk.Menu(menubar, tearoff=0, bg="#161b22", fg="#ffffff")
        self.menu_file.add_command(label="Exit", command=self.root.quit)
        menubar.add_cascade(menu=self.menu_file, label="File")

        self.menu_lang = tk.Menu(menubar, tearoff=0, bg="#161b22", fg="#ffffff")
        self.menu_lang.add_command(label="فارسی (Persian)", command=lambda: self.set_language("fa"))
        self.menu_lang.add_command(label="English", command=lambda: self.set_language("en"))
        self.menu_lang.add_command(label="العربية (Arabic)", command=lambda: self.set_language("ar"))
        menubar.add_cascade(menu=self.menu_lang, label="Language")

        self.menu_help = tk.Menu(menubar, tearoff=0, bg="#161b22", fg="#ffffff")
        self.menu_help.add_command(label="Donate (BEP-20)", command=self.show_donate_dialog)
        self.menu_help.add_separator()
        self.menu_help.add_command(label="About", command=self.show_about_dialog)
        menubar.add_cascade(menu=self.menu_help, label="Help")

        self.root.config(menu=menubar)

    def _build_ui(self):
        # ۱. بنر بالایی
        header_frame = tk.Frame(self.root, bg="#131b26", height=68, relief="groove", bd=1)
        header_frame.pack(fill="x", padx=10, pady=(8, 4))

        self.lbl_hero_title = ttk.Label(header_frame, text="NOVATRADE COPIER PRO", font=("Segoe UI", 14, "bold"),
                                        style="Header.TLabel")
        self.lbl_hero_title.pack(anchor="w", padx=15, pady=(8, 2))

        self.lbl_hero_sub = ttk.Label(header_frame, text="", font=("Segoe UI", 9), style="SubHeader.TLabel")
        self.lbl_hero_sub.pack(anchor="w", padx=15, pady=(0, 8))

        # نوار زبان
        top_bar = tk.Frame(self.root, bg="#0c1017")
        top_bar.pack(fill="x", padx=10, pady=2)

        self.lbl_lang = tk.Label(top_bar, text="", bg="#0c1017", fg="#8b949e", font=("Segoe UI", 9))
        self.lbl_lang.pack(side="left", padx=5)

        self.combo_lang = ttk.Combobox(top_bar, state="readonly", width=12, values=["فارسی", "English", "العربية"])
        self.combo_lang.current(0)
        self.combo_lang.pack(side="left", padx=5)
        self.combo_lang.bind("<<ComboboxSelected>>", self.on_lang_dropdown_change)

        # ۲. فریم ترمینال‌ها
        self.frame_terminals = ttk.LabelFrame(self.root, text="")
        self.frame_terminals.pack(fill="x", padx=10, pady=4)

        self.lbl_master = ttk.Label(self.frame_terminals, text="")
        self.lbl_master.grid(row=0, column=0, padx=8, pady=8, sticky="w")
        self.combo_master = ttk.Combobox(self.frame_terminals, state="readonly", width=35)
        self.combo_master.grid(row=0, column=1, padx=6, pady=8)

        self.lbl_slave = ttk.Label(self.frame_terminals, text="")
        self.lbl_slave.grid(row=0, column=2, padx=8, pady=8, sticky="w")
        self.combo_slave = ttk.Combobox(self.frame_terminals, state="readonly", width=35)
        self.combo_slave.grid(row=0, column=3, padx=6, pady=8)

        # ۳. فریم لات و ریسک
        self.frame_lot = ttk.LabelFrame(self.root, text="")
        self.frame_lot.pack(fill="x", padx=10, pady=4)

        self.lot_mode_var = tk.StringVar(value="Multiplier")
        self.rb_mult = ttk.Radiobutton(self.frame_lot, text="", variable=self.lot_mode_var, value="Multiplier")
        self.rb_mult.grid(row=0, column=0, padx=12, pady=6)

        self.rb_fixed = ttk.Radiobutton(self.frame_lot, text="", variable=self.lot_mode_var, value="Fixed")
        self.rb_fixed.grid(row=0, column=1, padx=12, pady=6)

        self.lbl_lot_val = ttk.Label(self.frame_lot, text="")
        self.lbl_lot_val.grid(row=0, column=2, padx=6, pady=6)
        self.ent_lot_val = ttk.Entry(self.frame_lot, width=10)
        self.ent_lot_val.insert(0, "1.0")
        self.ent_lot_val.grid(row=0, column=3, padx=6, pady=6)

        # ۴. فریم سمبل‌ها
        self.frame_symbols = ttk.LabelFrame(self.root, text="")
        self.frame_symbols.pack(fill="x", padx=10, pady=4)

        self.lbl_m_pre = ttk.Label(self.frame_symbols, text="")
        self.lbl_m_pre.grid(row=0, column=0, padx=5, pady=6)
        self.ent_m_pre = ttk.Entry(self.frame_symbols, width=7)
        self.ent_m_pre.grid(row=0, column=1, padx=5, pady=6)

        self.lbl_m_suf = ttk.Label(self.frame_symbols, text="")
        self.lbl_m_suf.grid(row=0, column=2, padx=5, pady=6)
        self.ent_m_suf = ttk.Entry(self.frame_symbols, width=7)
        self.ent_m_suf.grid(row=0, column=3, padx=5, pady=6)

        self.lbl_s_pre = ttk.Label(self.frame_symbols, text="")
        self.lbl_s_pre.grid(row=0, column=4, padx=5, pady=6)
        self.ent_s_pre = ttk.Entry(self.frame_symbols, width=7)
        self.ent_s_pre.grid(row=0, column=5, padx=5, pady=6)

        self.lbl_s_suf = ttk.Label(self.frame_symbols, text="")
        self.lbl_s_suf.grid(row=0, column=6, padx=5, pady=6)
        self.ent_s_suf = ttk.Entry(self.frame_symbols, width=7)
        self.ent_s_suf.grid(row=0, column=7, padx=5, pady=6)

        # ۵. فریم دونیت (حمایت مالی - بایننس اسمارت چین BEP-20)
        self.frame_donate = ttk.LabelFrame(self.root, text="")
        self.frame_donate.pack(fill="x", padx=10, pady=4)

        donate_inner = tk.Frame(self.frame_donate, bg="#131b26")
        donate_inner.pack(fill="x", padx=10, pady=6)

        self.lbl_wallet_address = tk.Label(donate_inner,
                                           text=f"BSC (BEP-20): {DONATE_WALLET_ADDRESS}",
                                           bg="#131b26", fg="#00e676", font=("Consolas", 10, "bold"))
        self.lbl_wallet_address.pack(side="left", padx=5)

        self.btn_copy_wallet = ttk.Button(donate_inner, text="", style="Donate.TButton", command=self.copy_wallet)
        self.btn_copy_wallet.pack(side="right", padx=5)

        # دکمه اعمال تنظیمات
        self.btn_apply = ttk.Button(self.root, text="", style="Primary.TButton", command=self.apply_settings)
        self.btn_apply.pack(fill="x", padx=10, pady=6)

        # ۶. فریم لاگ و مانیتورینگ زنده (با فونت استاندارد و خوش‌فرم فارسی)
        self.frame_log = ttk.LabelFrame(self.root, text="")
        self.frame_log.pack(fill="both", expand=True, padx=10, pady=(2, 8))

        log_ctrl_bar = tk.Frame(self.frame_log, bg="#131b26")
        log_ctrl_bar.pack(fill="x", padx=5, pady=2)

        self.btn_clear_log = ttk.Button(log_ctrl_bar, text="", style="Secondary.TButton", command=self.clear_logs)
        self.btn_clear_log.pack(side="right", padx=4)

        # فونت اصلاح‌شده: Segoe UI با فال‌بک Tahoma برای رندر بی‌نقص حروف فارسی و عدم تکه‌تکه شدن
        global log_area
        log_area = scrolledtext.ScrolledText(
            self.frame_log,
            wrap=tk.WORD,
            height=12,
            bg="#0d1117",
            fg="#58a6ff",
            insertbackground="#ffffff",
            font=("Segoe UI", 9),
            relief="flat",
            padx=8,
            pady=6
        )
        log_area.pack(fill="both", expand=True, padx=6, pady=4)

    def set_language(self, lang_code):
        app_config["lang"] = lang_code
        mapping = {"fa": 0, "en": 1, "ar": 2}
        self.combo_lang.current(mapping.get(lang_code, 0))
        self.apply_language_texts()

    def on_lang_dropdown_change(self, event=None):
        sel = self.combo_lang.get()
        if sel == "فارسی":
            self.set_language("fa")
        elif sel == "English":
            self.set_language("en")
        elif sel == "العربية":
            self.set_language("ar")

    def apply_language_texts(self):
        self.root.title(get_text("title"))
        self.lbl_hero_sub.config(text=get_text("hero_sub"))
        self.lbl_lang.config(text=get_text("lang_lbl"))

        # منوها
        self.menu_file.entryconfig(0, label=get_text("menu_exit"))
        self.menu_help.entryconfig(0, label=get_text("menu_donate"))
        self.menu_help.entryconfig(2, label=get_text("menu_about"))

        # ترمینال‌ها
        self.frame_terminals.config(text=get_text("frame_terminals"))
        self.lbl_master.config(text=get_text("master_lbl"))
        self.lbl_slave.config(text=get_text("slave_lbl"))

        # لات
        self.frame_lot.config(text=get_text("frame_lot"))
        self.rb_mult.config(text=get_text("lot_mult"))
        self.rb_fixed.config(text=get_text("lot_fixed"))
        self.lbl_lot_val.config(text=get_text("lot_val"))

        # نمادها
        self.frame_symbols.config(text=get_text("frame_symbols"))
        self.lbl_m_pre.config(text=get_text("m_pre"))
        self.lbl_m_suf.config(text=get_text("m_suf"))
        self.lbl_s_pre.config(text=get_text("s_pre"))
        self.lbl_s_suf.config(text=get_text("s_suf"))

        # دونیت
        self.frame_donate.config(text=get_text("frame_donate"))
        self.btn_copy_wallet.config(text=get_text("btn_copy_wallet"))

        # دکمه و لاگ
        self.btn_apply.config(text=get_text("btn_apply"))
        self.frame_log.config(text=get_text("frame_log"))
        self.btn_clear_log.config(text=get_text("btn_clear_log"))

    def copy_wallet(self):
        self.root.clipboard_clear()
        self.root.clipboard_append(DONATE_WALLET_ADDRESS)
        messagebox.showinfo("NovaTrade Copier", get_text("wallet_copied"))

    def show_donate_dialog(self):
        self.copy_wallet()

    def show_about_dialog(self):
        messagebox.showinfo("About NovaTrade Copier", get_text("about_text"))

    def clear_logs(self):
        log_area.delete('1.0', tk.END)

    def apply_settings(self):
        app_config["master_id"] = self.combo_master.get().split(" - ")[0] if self.combo_master.get() else ""
        app_config["slave_id"] = self.combo_slave.get().split(" - ")[0] if self.combo_slave.get() else ""
        app_config["lot_mode"] = self.lot_mode_var.get()
        try:
            app_config["lot_value"] = float(self.ent_lot_val.get() or 1.0)
        except ValueError:
            app_config["lot_value"] = 1.0

        app_config["master_prefix"] = self.ent_m_pre.get().strip()
        app_config["master_suffix"] = self.ent_m_suf.get().strip()
        app_config["slave_prefix"] = self.ent_s_pre.get().strip()
        app_config["slave_suffix"] = self.ent_s_suf.get().strip()

        log_event(get_text("applied").format(master=app_config['master_id'], slave=app_config['slave_id']))

    def update_terminals_list(self):
        current_options = [f"{t_id} - {data['platform']} ({data['account']})" for t_id, data in terminals_data.items()]
        self.combo_master['values'] = current_options
        self.combo_slave['values'] = current_options
        self.root.after(1000, self.update_terminals_list)


if __name__ == "__main__":
    t = threading.Thread(target=file_watcher_loop, daemon=True)
    t.start()

    root = tk.Tk()
    app = CopierGUI(root)
    log_event(f"{get_text('ready')} {COMMON_FILES_DIR}")
    root.mainloop()
