import sqlite3
from contextlib import contextmanager

from database.connections.connection import DatabaseConnection

class SQLiteConnection(DatabaseConnection):
    def __init__(self, db_path="documents.db"):
        """Initialize the SQLite database and create tables if needed."""
        self.conn = None
        self.db_path = db_path
        self._init_db()

    def _init_db(self):
        return self._create_tables()

    def _create_tables(self):
        """Create tables for documents and settings."""
        conn = sqlite3.connect(self.db_path, check_same_thread=False)
        cursor = conn.cursor()

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS documents (
            id TEXT PRIMARY KEY,
            content TEXT,
            description TEXT,
            timestamp TIMESTAMP,
            filetype TEXT
        )
        """)

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS settings (
            key TEXT PRIMARY KEY,
            value TEXT
        )
        """)
        conn.commit()
    
    @contextmanager
    def get_connection(self):
        """Get a database connection with context management"""
        if self.conn is None:
            self.conn = sqlite3.connect(self.db_path, check_same_thread=False)
            self.conn.row_factory = sqlite3.Row

        yield self.conn

    def close(self):
        """Close the database connection."""
        self.conn.close()
        self.conn = None

    ## SETTINGS CRUD
    # def set_setting(self, key, value):
    #     """Store a key-value setting."""
    #     self.cursor.execute("INSERT INTO settings (key, value) VALUES (?, ?) ON CONFLICT(key) DO UPDATE SET value = ?",
    #                         (key, value, value))
    #     self.conn.commit()

    # def get_setting(self, key):
    #     """Retrieve a setting by key."""
    #     self.cursor.execute("SELECT value FROM settings WHERE key = ?", (key,))
    #     setting = self.cursor.fetchone()
    #     return setting[0] if setting else None