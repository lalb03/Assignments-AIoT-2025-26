
import sqlite3

DB_FILE = 'bot_data.db'

def init_db():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Measurements (
            timestamp DATETIME NOT NULL PRIMARY KEY,
            temperature REAL NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

def insert_measurement(timestamp, temperature):
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()

    cursor.execute('''
        INSERT INTO Measurements (timestamp, temperature) VALUES (?, ?)
    ''', (timestamp, temperature))
    conn.commit()
    conn.close()

def get_average():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()

    cursor.execute('SELECT AVG(temperature), COUNT(*) FROM Measurements')
    row = cursor.fetchone()
    conn.close()
    if row is None:
        return None, 0
    avg_temp, count = row
    return avg_temp, count

def get_min():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()

    cursor.execute('SELECT timestamp, temperature FROM Measurements ORDER BY temperature ASC LIMIT 1')
    row = cursor.fetchone()
    conn.close()
    if row is None:
        return None
    timestamp, min_temp = row
    return timestamp, min_temp

def get_max():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()

    cursor.execute('SELECT timestamp, temperature FROM Measurements ORDER BY temperature DESC LIMIT 1')
    row = cursor.fetchone()
    conn.close()
    if row is None:
        return None
    timestamp, max_temp = row
    return timestamp, max_temp

def get_history():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()

    cursor.execute('SELECT timestamp, temperature FROM Measurements ORDER BY timestamp DESC LIMIT 10')
    rows = cursor.fetchall()
    conn.close()
    return rows