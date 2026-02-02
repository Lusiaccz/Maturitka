import sqlite3
import datetime

def init_db():
    conn = sqlite3.connect("tetris.db")
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS high_scores 
                      (id INTEGER PRIMARY KEY AUTOINCREMENT, 
                       name TEXT, score INTEGER, level INTEGER, played_at TEXT)''')
    conn.commit()
    conn.close()

def save_score(name, score, level):
    conn = sqlite3.connect("tetris.db")
    cursor = conn.cursor()
    cas_ted = datetime.datetime.now().strftime("%d.%m.%Y %H:%M")
    cursor.execute("INSERT INTO high_scores (name, score, level, played_at) VALUES (?, ?, ?, ?)",
                   (name, score, level, cas_ted))
    conn.commit()
    conn.close()