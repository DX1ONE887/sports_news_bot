import sqlite3
from config import DATABASE_NAME

def init_db():
    with sqlite3.connect(DATABASE_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS stop_words (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                word TEXT NOT NULL UNIQUE
            )
        ''')
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS sources (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                url TEXT NOT NULL UNIQUE
            )
        ''')
        conn.commit()

def remove_stop_word(word_id: int):
    with sqlite3.connect(DATABASE_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute('DELETE FROM stop_words WHERE id = ?', (word_id,))
        conn.commit()

def remove_source(source_id: int):
    with sqlite3.connect(DATABASE_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute('DELETE FROM sources WHERE id = ?', (source_id,))
        conn.commit()

def get_all_stop_words():
    with sqlite3.connect(DATABASE_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT id, word FROM stop_words ORDER BY id')
        return cursor.fetchall()

def get_all_sources():
    with sqlite3.connect(DATABASE_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT id, url FROM sources ORDER BY id')
        return cursor.fetchall()

def add_stop_word(word: str):
    with sqlite3.connect(DATABASE_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute('INSERT OR IGNORE INTO stop_words (word) VALUES (?)', (word.lower(),))
        conn.commit()

def get_stop_words():
    with sqlite3.connect(DATABASE_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT word FROM stop_words')
        return [row[0] for row in cursor.fetchall()]

def add_source(url: str):
    with sqlite3.connect(DATABASE_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute('INSERT OR IGNORE INTO sources (url) VALUES (?)', (url,))
        conn.commit()

def get_sources():
    with sqlite3.connect(DATABASE_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT url FROM sources')
        return [row[0] for row in cursor.fetchall()]

init_db()