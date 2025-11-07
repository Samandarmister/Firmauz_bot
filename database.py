import sqlite3
import os
from config import DATA_PATH
import asyncio
import logging

logger = logging.getLogger(__name__)

def init_db():
    try:
        conn = sqlite3.connect(os.path.join(DATA_PATH, "bot.db"))
        c = conn.cursor()
        # Mavjud jadvallar
        c.execute('''CREATE TABLE IF NOT EXISTS users (
            user_id INTEGER PRIMARY KEY,
            language TEXT DEFAULT 'uz_latin'
        )''')
        c.execute('''CREATE TABLE IF NOT EXISTS firms (
            stir TEXT PRIMARY KEY,
            name TEXT,
            rahbar TEXT,
            soliq_turi TEXT,
            ds_stavka TEXT,
            ys_stavka TEXT,
            qqs_stavka TEXT
        )''')
        c.execute('''CREATE TABLE IF NOT EXISTS reports (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            stir TEXT,
            oy TEXT,
            firma_name TEXT,
            xodimlar_soni INTEGER,
            xodimlar_data TEXT,
            hisobot_davri_oylik INTEGER,
            jami_oylik INTEGER,
            soliq INTEGER
        )''')
        c.execute('''CREATE TABLE IF NOT EXISTS reports_yagona (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            stir TEXT,
            oy TEXT,
            firma_name TEXT,
            rahbar TEXT,
            soliq_turi_yagona TEXT,
            yil_boshidan_aylanma INTEGER,
            shu_oy_aylanma INTEGER,
            yagona_soliq INTEGER
        )''')
        c.execute('''CREATE TABLE IF NOT EXISTS reports_qqs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            stir TEXT,
            oy TEXT,
            firma_name TEXT,
            rahbar TEXT,
            soliq_turi_qqs TEXT,
            yil_boshidan_qqs INTEGER,
            shu_oy_qqs INTEGER,
            qqs_soliq INTEGER
        )''')
        c.execute('''CREATE TABLE IF NOT EXISTS files (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            stir TEXT,
            soliq_turi TEXT,
            oy TEXT,
            file_type TEXT,
            file_path TEXT
        )''')
        c.execute('''CREATE TABLE IF NOT EXISTS firm_docs (
            stir TEXT PRIMARY KEY,
            pdf1 TEXT,
            pdf2 TEXT,
            pfx TEXT
        )''')
        conn.commit()
        conn.close()
        logger.info("Ma'lumotlar bazasi muvaffaqiyatli yangilandi.")
    except Exception as e:
        logger.error(f"Ma'lumotlar bazasi yangilashda xato: {e}")

def init_security_tables():
    conn = sqlite3.connect(os.path.join(DATA_PATH, "bot.db"))
    c = conn.cursor()

    # Firma egasi telefon bazasi
    c.execute("""
        CREATE TABLE IF NOT EXISTS firm_owners (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            stir TEXT,
            phone TEXT
        )
    """)

    # Yuklab olish logi
    c.execute("""
        CREATE TABLE IF NOT EXISTS downloads_log (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id TEXT,
            phone TEXT,
            stir TEXT,
            file_type TEXT,
            downloaded_at DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    """)

    # Xavfsizlik alert jadvali
    c.execute("""
        CREATE TABLE IF NOT EXISTS security_alerts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id TEXT,
            phone TEXT,
            stir TEXT,
            event TEXT,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    """)

    c.execute("""
        CREATE TABLE IF NOT EXISTS firm_access_log (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            stir TEXT,
            phone TEXT,
            timestamp INTEGER
        )
    """)

    conn.commit()
    conn.close()


MAX_CHECKS = 10
BLOCK_SECONDS = 24 * 60 * 60

def log_access_attempt(stir, phone, user_id):
    conn = sqlite3.connect(os.path.join(DATA_PATH, "bot.db"))
    c = conn.cursor()
    c.execute("""
        INSERT INTO firm_access_log (stir, phone, user_id, timestamp)
        VALUES (?, ?, ?, strftime('%s','now'))
    """, (stir, phone, user_id))
    conn.commit()
    conn.close()


def is_blocked(stir, user_id):
    conn = sqlite3.connect(os.path.join(DATA_PATH, "bot.db"))
    c = conn.cursor()
    c.execute("""
        SELECT COUNT(*) FROM firm_access_log
        WHERE stir=? AND user_id=? AND timestamp > strftime('%s','now') - ?
    """, (stir, user_id, BLOCK_SECONDS))
    count = c.fetchone()[0]
    conn.close()
    return count >= MAX_CHECKS






def add_firm_owner(stir, phone):
    conn = sqlite3.connect(os.path.join(DATA_PATH, "bot.db"))
    c = conn.cursor()
    c.execute("INSERT INTO firm_owners (stir, phone) VALUES (?,?)", (stir, phone))
    conn.commit()
    conn.close()


def verify_owner_phone(stir, phone):
    conn = sqlite3.connect(os.path.join(DATA_PATH, "bot.db"))
    c = conn.cursor()
    c.execute("SELECT id FROM firm_owners WHERE stir=? AND phone=?", (stir, phone))
    result = c.fetchone()
    conn.close()
    return result is not None



def log_download(uid, phone, stir, file):
    conn = sqlite3.connect(os.path.join(DATA_PATH, "bot.db"))
    c = conn.cursor()
    c.execute("INSERT INTO downloads_log (user_id, phone, stir, file_type) VALUES (?,?,?,?)",
             (uid, phone, stir, file))
    conn.commit()
    conn.close()



def today_downloads(phone, stir):
    conn = sqlite3.connect(os.path.join(DATA_PATH, "bot.db"))
    c = conn.cursor()
    c.execute("""
        SELECT COUNT(*) FROM downloads_log 
        WHERE phone=? AND stir=? AND DATE(downloaded_at)=DATE('now')
    """, (phone, stir))
    cnt = c.fetchone()[0]
    conn.close()
    return cnt


def log_alert(uid, phone, stir, event):
    conn = sqlite3.connect(os.path.join(DATA_PATH, "bot.db"))
    c = conn.cursor()
    c.execute("INSERT INTO security_alerts (user_id, phone, stir, event) VALUES (?,?,?,?)",
             (uid, phone, stir, event))
    conn.commit()
    conn.close()


def save_firm_docs(stir, pdf1, pdf2, pfx):
    conn = sqlite3.connect(os.path.join(DATA_PATH, "bot.db"))
    c = conn.cursor()
    c.execute("""
        INSERT OR REPLACE INTO firm_docs (stir, pdf1, pdf2, pfx)
        VALUES (?, ?, ?, ?)
    """, (stir, pdf1, pdf2, pfx))
    conn.commit()
    conn.close()

def get_firm_docs(stir):
    conn = sqlite3.connect(os.path.join(DATA_PATH, "bot.db"))
    c = conn.cursor()
    c.execute("SELECT pdf1, pdf2, pfx FROM firm_docs WHERE stir=?", (stir,))
    result = c.fetchone()
    conn.close()
    return result


def get_owner_phone(stir):
    conn = sqlite3.connect(os.path.join(DATA_PATH, "bot.db"))
    c = conn.cursor()
    c.execute("SELECT phone FROM firm_owners WHERE stir=?", (stir,))
    row = c.fetchone()
    conn.close()
    return row[0] if row else None


def save_yagona_report(stir, oy, firma_name, rahbar, soliq_turi_yagona, yil_boshidan_aylanma, shu_oy_aylanma, yagona_soliq):
    conn = sqlite3.connect(os.path.join(DATA_PATH, "bot.db"))
    c = conn.cursor()
    c.execute("""
        INSERT INTO reports_yagona (stir, oy, firma_name, rahbar, soliq_turi_yagona, yil_boshidan_aylanma, shu_oy_aylanma, yagona_soliq)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, (stir, oy, firma_name, rahbar, soliq_turi_yagona, yil_boshidan_aylanma, shu_oy_aylanma, yagona_soliq))
    conn.commit()
    conn.close()

def save_qqs_report(stir, oy, firma_name, rahbar, soliq_turi_qqs, yil_boshidan_qqs, shu_oy_qqs, qqs_soliq):
    conn = sqlite3.connect(os.path.join(DATA_PATH, "bot.db"))
    c = conn.cursor()
    c.execute("""
        INSERT INTO reports_qqs (stir, oy, firma_name, rahbar, soliq_turi_qqs, yil_boshidan_qqs, shu_oy_qqs, qqs_soliq)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, (stir, oy, firma_name, rahbar, soliq_turi_qqs, yil_boshidan_qqs, shu_oy_qqs, qqs_soliq))
    conn.commit()
    conn.close()

def get_yagona_report(stir, oy):
    conn = sqlite3.connect(os.path.join(DATA_PATH, "bot.db"))
    c = conn.cursor()
    c.execute("SELECT * FROM reports_yagona WHERE stir = ? AND oy = ?", (stir, oy))
    result = c.fetchone()
    conn.close()
    return result

def get_qqs_report(stir, oy):
    conn = sqlite3.connect(os.path.join(DATA_PATH, "bot.db"))
    c = conn.cursor()
    c.execute("SELECT * FROM reports_qqs WHERE stir = ? AND oy = ?", (stir, oy))
    result = c.fetchone()
    conn.close()
    return result



def add_firma(stir, name, rahbar=None, soliq_turi=None, ds_stavka=None, ys_stavka=None, qqs_stavka=None):
    conn = sqlite3.connect(os.path.join(DATA_PATH, "bot.db"))
    c = conn.cursor()
    c.execute("INSERT INTO firms (stir, name, rahbar, soliq_turi, ds_stavka, ys_stavka, qqs_stavka) VALUES (?, ?, ?, ?, ?, ?, ?)",
              (stir, name, rahbar, soliq_turi, ds_stavka, ys_stavka, qqs_stavka))
    conn.commit()
    conn.close()

def get_firma_info(stir):
    conn = sqlite3.connect(os.path.join(DATA_PATH, "bot.db"))
    c = conn.cursor()
    c.execute("SELECT name, rahbar, soliq_turi, ds_stavka, ys_stavka, qqs_stavka FROM firms WHERE stir = ?", (stir,))
    result = c.fetchone()
    conn.close()
    return result


def check_firma(stir):
    conn = sqlite3.connect(os.path.join(DATA_PATH, "bot.db"))
    c = conn.cursor()
    c.execute("SELECT stir FROM firms WHERE stir = ?", (stir,))
    result = c.fetchone()
    conn.close()
    return result is not None

def get_all_firms():
    conn = sqlite3.connect(os.path.join(DATA_PATH, "bot.db"))
    c = conn.cursor()
    c.execute("SELECT stir, name FROM firms ORDER BY name ASC")
    firms = c.fetchall()
    conn.close()
    return [(str(stir), str(name).lower() if name else "") for stir, name in firms]



def get_firma_name(stir):
    conn = sqlite3.connect(os.path.join(DATA_PATH, "bot.db"))
    c = conn.cursor()
    c.execute("SELECT name FROM firms WHERE stir = ?", (stir,))
    result = c.fetchone()
    conn.close()
    return result[0] if result else "Noma'lum"

def save_file(stir, soliq_turi, oy, file_type, file_path):
    try:
        conn = sqlite3.connect(os.path.join(DATA_PATH, "bot.db"))
        c = conn.cursor()
        c.execute("INSERT OR REPLACE INTO files (stir, soliq_turi, oy, file_type, file_path) VALUES (?, ?, ?, ?, ?)",
                 (stir, soliq_turi, oy.lower(), file_type, file_path))
        conn.commit()
        logger.info(f"Fayl saqlandi: stir={stir}, soliq_turi={soliq_turi}, oy={oy}, file_type={file_type}, file_path={file_path}")
    except sqlite3.Error as e:
        logger.error(f"SQL xatosi faylni saqlashda: {e}, stir={stir}, soliq_turi={soliq_turi}, oy={oy}, file_type={file_type}")
    finally:
        conn.close()

def check_file(stir, soliq_turi, oy, file_type):
    try:
        conn = sqlite3.connect(os.path.join(DATA_PATH, "bot.db"))
        c = conn.cursor()
        c.execute("SELECT file_path FROM files WHERE stir=? AND soliq_turi=? AND oy=? AND file_type=?", 
                 (stir, soliq_turi, oy.lower(), file_type))
        result = c.fetchone()
        logger.info(f"check_file: stir={stir}, soliq_turi={soliq_turi}, oy={oy}, file_type={file_type}, result={result}")
        return result[0] if result else None
    except sqlite3.Error as e:
        logger.error(f"check_file xatosi: {e}, stir={stir}, soliq_turi={soliq_turi}, oy={oy}, file_type={file_type}")
        return None
    finally:
        conn.close()


def save_manual_report(stir, oy, firma_name, xodimlar_soni, xodimlar_data, hisobot_davri_oylik, jami_oylik, soliq):
    conn = sqlite3.connect(os.path.join(DATA_PATH, "bot.db"))
    c = conn.cursor()
    c.execute("""
        INSERT INTO reports (stir, oy, firma_name, xodimlar_soni, xodimlar_data, hisobot_davri_oylik, jami_oylik, soliq)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, (stir, oy, firma_name, xodimlar_soni, xodimlar_data, hisobot_davri_oylik, jami_oylik, soliq))
    conn.commit()
    conn.close()

def get_manual_report(stir, oy):
    conn = sqlite3.connect(os.path.join(DATA_PATH, "bot.db"))
    c = conn.cursor()
    c.execute("SELECT * FROM reports WHERE stir = ? AND oy = ?", (stir, oy))
    result = c.fetchone()
    conn.close()
    return result

def set_user_language(user_id, language):
    try:
        # language qiymatini uz_cyrillic yoki uz_latin bilan almashtiramiz
        if language == 'cyrillic':
            language = 'uz_cyrillic'
        elif language == 'latin':
            language = 'uz_latin'
        conn = sqlite3.connect(os.path.join(DATA_PATH, "bot.db"))
        c = conn.cursor()
        c.execute("INSERT OR REPLACE INTO users (user_id, language) VALUES (?, ?)", (user_id, language))
        conn.commit()
        conn.close()
        logger.info(f"set_user_language: user_id={user_id}, language={language}")
    except Exception as e:
        logger.error(f"set_user_language xatosi: {e}")

def get_user_language(user_id):
    try:
        conn = sqlite3.connect(os.path.join(DATA_PATH, "bot.db"))
        c = conn.cursor()
        c.execute("SELECT language FROM users WHERE user_id = ?", (user_id,))
        result = c.fetchone()
        conn.close()
        lang = result[0] if result else 'uz_latin'
        # cyrillic ni uz_cyrillic bilan almashtiramiz
        if lang == 'cyrillic':
            lang = 'uz_cyrillic'
        logger.info(f"get_user_language: user_id={user_id}, lang={lang}")
        return lang
    except Exception as e:
        logger.error(f"get_user_language xatosi: {e}")
        return 'uz_latin'
    


def update_firm_phone(stir, phone):
    conn = sqlite3.connect(os.path.join(DATA_PATH, "bot.db"))
    c = conn.cursor()
    c.execute("UPDATE firm_owners SET phone=? WHERE stir=?", (phone, stir))
    conn.commit()
    conn.close()


async def cleanup_access_logs():
    conn = sqlite3.connect(os.path.join(DATA_PATH, "bot.db"))
    c = conn.cursor()
    c.execute(
        "DELETE FROM firm_access_log WHERE timestamp <= strftime('%s','now') - ?",
        (BLOCK_SECONDS,)
    )
    conn.commit()
    conn.close()
