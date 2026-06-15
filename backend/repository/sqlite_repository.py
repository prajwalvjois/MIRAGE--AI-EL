import sqlite3
import uuid
from typing import List
from backend.core.interfaces.irepository import IRepository
from backend.core.models.threat_event import ThreatEvent

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
                    brand TEXT,
                    risk_score REAL,
                    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            try:
                cursor.execute('ALTER TABLE email_events ADD COLUMN brand TEXT')
            except sqlite3.OperationalError:
                pass
                
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS url_events (
                    id TEXT PRIMARY KEY,
                    url TEXT,
                    brand TEXT,
                    risk_score REAL,
                    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            try:
                cursor.execute('ALTER TABLE url_events ADD COLUMN brand TEXT')
            except sqlite3.OperationalError:
                pass
                
            conn.commit()

    def save_email_event(self, email_text: str, brand: str, risk_score: float) -> str:
        event_id = str(uuid.uuid4())
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(
                'INSERT INTO email_events (id, email_text, brand, risk_score) VALUES (?, ?, ?, ?)', 
                (event_id, email_text, brand, risk_score)
            )
            conn.commit()
        return event_id

    def save_url_event(self, url: str, brand: str, risk_score: float) -> str:
        event_id = str(uuid.uuid4())
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(
                'INSERT INTO url_events (id, url, brand, risk_score) VALUES (?, ?, ?, ?)', 
                (event_id, url, brand, risk_score)
            )
            conn.commit()
        return event_id

    def get_recent_events(self, limit: int = 100) -> List[ThreatEvent]:
        events = []
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT id, 'EMAIL' as event_type, risk_score, brand, timestamp 
                FROM email_events 
                UNION ALL 
                SELECT id, 'URL' as event_type, risk_score, brand, timestamp 
                FROM url_events 
                ORDER BY timestamp DESC 
                LIMIT ?
            ''', (limit,))
            rows = cursor.fetchall()
            for row in rows:
                brand_val = row[3] if row[3] is not None else "Unknown"
                events.append(ThreatEvent(
                    event_id=row[0],
                    event_type=row[1],
                    risk_score=row[2],
                    brand=brand_val,
                    timestamp=row[4]
                ))
        return events
