import sqlite3
from typing import Optional, Dict, List

def connect(db_path: str) -> sqlite3.Connection:
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    return conn

def init_db(conn: sqlite3.Connection) -> None:
    cur = conn.cursor()
    cur.execute("""
    CREATE TABLE IF NOT EXISTS tasks (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        chat_id INTEGER NOT NULL,
        task_text TEXT NOT NULL,
        status TEXT NOT NULL DEFAULT 'OPEN',
        created_at TEXT NOT NULL DEFAULT (datetime('now')),
        closed_at TEXT
    );
    """)
    cur.execute("""
    CREATE TABLE IF NOT EXISTS task_outputs (
        task_id INTEGER PRIMARY KEY,
        roadmap_v1 TEXT NOT NULL,
        elon_review TEXT NOT NULL,
        FOREIGN KEY(task_id) REFERENCES tasks(id)
    );
    """)
    conn.commit()

def create_task(
    conn: sqlite3.Connection,
    chat_id: int,
    task_text: str,
    roadmap_v1: str,
    elon_review: str
) -> int:
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO tasks (chat_id, task_text) VALUES (?, ?)",
        (chat_id, task_text.strip())
    )
    task_id = cur.lastrowid
    cur.execute(
        "INSERT INTO task_outputs (task_id, roadmap_v1, elon_review) VALUES (?, ?, ?)",
        (task_id, roadmap_v1, elon_review)
    )
    conn.commit()
    return int(task_id)

def list_open_tasks(conn: sqlite3.Connection, chat_id: int) -> List[sqlite3.Row]:
    cur = conn.cursor()
    cur.execute(
        "SELECT id, task_text, created_at FROM tasks "
        "WHERE chat_id=? AND status='OPEN' ORDER BY id DESC",
        (chat_id,)
    )
    return cur.fetchall()

def close_task(conn: sqlite3.Connection, chat_id: int, task_id: int) -> bool:
    cur = conn.cursor()
    cur.execute(
        "UPDATE tasks SET status='DONE', closed_at=datetime('now') "
        "WHERE chat_id=? AND id=? AND status='OPEN'",
        (chat_id, task_id)
    )
    conn.commit()
    return cur.rowcount > 0

def get_task(conn: sqlite3.Connection, chat_id: int, task_id: int) -> Optional[Dict]:
    cur = conn.cursor()
    cur.execute("""
        SELECT t.id, t.task_text, t.status, t.created_at, t.closed_at,
               o.roadmap_v1, o.elon_review
        FROM tasks t
        JOIN task_outputs o ON o.task_id = t.id
        WHERE t.chat_id=? AND t.id=?
    """, (chat_id, task_id))
    row = cur.fetchone()
    return dict(row) if row else None

