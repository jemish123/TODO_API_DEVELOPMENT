# backend/app/models/todo_model.py
from app.database.connection import get_connection
from datetime import datetime

def get_all_todos():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM todos ORDER BY created_at DESC")
    rows = cur.fetchall()
    columns = [desc[0] for desc in cur.description]
    todos = [dict(zip(columns, row)) for row in rows]
    cur.close()
    conn.close()
    return todos

def create_todo(title, description):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        """
        INSERT INTO todos (title, description)
        VALUES (%s, %s)
        RETURNING *
        """,
        (title, description)
    )
    row = cur.fetchone()
    columns = [desc[0] for desc in cur.description]
    conn.commit()
    cur.close()
    conn.close()
    return dict(zip(columns, row))

def update_todo_status(todo_id, status):
    conn = get_connection()
    cur = conn.cursor()
    completed_at = datetime.utcnow() if status == 'completed' else None
    cur.execute(
        """
        UPDATE todos
        SET status = %s, completed_at = %s
        WHERE id = %s
        RETURNING *
        """,
        (status, completed_at, todo_id)
    )
    row = cur.fetchone()
    columns = [desc[0] for desc in cur.description] if row else []
    conn.commit()
    cur.close()
    conn.close()
    return dict(zip(columns, row)) if row else None

def delete_todo(todo_id):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM todos WHERE id = %s", (todo_id,))
    conn.commit()
    cur.close()
    conn.close()
    return True
