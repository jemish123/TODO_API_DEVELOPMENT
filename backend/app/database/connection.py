import psycopg2
import os


DB_URL = os.getenv('DATABASE_URL', "dbname=todo_db user=postgres password=1234 host=localhost")

def get_connection():
    return psycopg2.connect(DB_URL)

def init_db():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS todos (
            id SERIAL PRIMARY KEY,
            title TEXT NOT NULL,
            description TEXT,
            status TEXT DEFAULT 'pending',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            completed_at TIMESTAMP
        );
    """)
    conn.commit()
    cur.close()
    conn.close()
