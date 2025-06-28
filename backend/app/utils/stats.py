from app.database.connection import get_connection


def get_stats():
    conn = get_connection()
    cur = conn.cursor()
    
    cur.execute("SELECT status, COUNT(*) FROM todos GROUP BY status")
    status_counts = {row[0]: row[1] for row in cur.fetchall()}
    
    cur.execute("""
        SELECT EXTRACT (EPOCH FROM (completed_at - created_at)) / 60 as duration
        FROM todos
        WHERE status='completed' AND completed_at IS NOT NULL
    """)
    durations = [duration[0] for duration in cur.fetchall() if duration[0] is not None]
    
    cur.close()
    conn.close()
    
    return {
        "completed": status_counts.get('completed', 0),
        "pending": status_counts.get('pending', 0),
        "cancelled": status_counts.get('cancelled', 0),
        "avg_time": round(sum(durations) / len(durations), 2) if durations else 0
    }