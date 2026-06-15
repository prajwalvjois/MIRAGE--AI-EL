import sqlite3
import uuid
from backend.core.interfaces.irepository import IRepository

class SQLiteRepository(IRepository):
    def __init__(self, db_path: str = "mirage.db"):
        self.db_path = db_path
        self._init_db()
        
    def _init_db(self):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS email_events (
                    id TEXT PRIMARY KEY,
                    email_text TEXT,
                    risk_score REAL,
                    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS url_events (
                    id TEXT PRIMARY KEY,
                    url TEXT,
                    risk_score REAL,
                    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            conn.commit()

    def save_email_event(self, email_text: str, risk_score: float) -> str:
        event_id = str(uuid.uuid4())
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(
                'INSERT INTO email_events (id, email_text, risk_score) VALUES (?, ?, ?)', 
                (event_id, email_text, risk_score)
            )
            conn.commit()
        return event_id

    def save_url_event(self, url: str, risk_score: float) -> str:
        event_id = str(uuid.uuid4())
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(
                'INSERT INTO url_events (id, url, risk_score) VALUES (?, ?, ?)', 
                (event_id, url, risk_score)
            )
            conn.commit()
        return event_id
