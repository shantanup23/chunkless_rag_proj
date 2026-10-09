import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "documents.db")

def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS documents (
            doc_id TEXT PRIMARY KEY,
            filename TEXT,
            markdown_content TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()

def save_document(doc_id: str, filename: str, markdown_content: str):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO documents (doc_id, filename, markdown_content)
        VALUES (?, ?, ?)
    ''', (doc_id, filename, markdown_content))
    conn.commit()
    conn.close()

def get_document(doc_id: str):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('SELECT filename, markdown_content FROM documents WHERE doc_id = ?', (doc_id,))
    row = cursor.fetchone()
    conn.close()
    if row:
        return {"filename": row[0], "markdown_content": row[1]}
    return None
