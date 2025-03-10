import sqlite3
from datetime import datetime
from typing import List, Dict

class ChatDatabase:
    def __init__(self, db_path: str = 'chat_history.db'):
        self.db_path = db_path
        self._init_db()

    def _init_db(self):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS chat_history (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    query TEXT NOT NULL,
                    category TEXT NOT NULL,
                    sentiment TEXT NOT NULL,
                    response TEXT NOT NULL,
                    conversation_id TEXT NOT NULL,
                    parent_id INTEGER,
                    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (parent_id) REFERENCES chat_history(id)
                )
            """)
            conn.commit()

    def add_interaction(self, query: str, category: str, sentiment: str, response: str, conversation_id: str = None, parent_id: int = None) -> int:
        if conversation_id is None:
            conversation_id = datetime.now().strftime('%Y%m%d%H%M%S')
        
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO chat_history (query, category, sentiment, response, conversation_id, parent_id) VALUES (?, ?, ?, ?, ?, ?)",
                (query, category, sentiment, response, conversation_id, parent_id)
            )
            conn.commit()
            return cursor.lastrowid

    def get_conversation_history(self, conversation_id: str) -> List[Dict]:
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            cursor.execute(
                "SELECT * FROM chat_history WHERE conversation_id = ? ORDER BY timestamp ASC",
                (conversation_id,)
            )
            rows = cursor.fetchall()
            return [dict(row) for row in rows]

    def get_last_interaction(self, conversation_id: str) -> Dict:
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            cursor.execute(
                "SELECT * FROM chat_history WHERE conversation_id = ? ORDER BY timestamp DESC LIMIT 1",
                (conversation_id,)
            )
            row = cursor.fetchone()
            return dict(row) if row else None

    def get_chat_history(self, limit: int = 10) -> List[Dict]:
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            cursor.execute(
                "SELECT * FROM chat_history ORDER BY timestamp DESC LIMIT ?",
                (limit,)
            )
            rows = cursor.fetchall()
            return [dict(row) for row in rows]

    def clear_history(self) -> None:
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM chat_history")
            conn.commit()