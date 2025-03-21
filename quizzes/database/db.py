"""
SQLite database module for quiz application.
Handles connection and initialization of the database.
"""
import os
import sqlite3
from pathlib import Path

# Get the project root directory
ROOT_DIR = Path(__file__).parent.parent.parent
DB_FILE = os.path.join(ROOT_DIR, 'quiz_data.db')

def get_connection():
    """
    Create a connection to the SQLite database.
    Returns the connection object.
    """
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row  # Makes rows accessible by column name
    return conn

def init_db():
    """
    Initialize the database by creating necessary tables if they don't exist.
    """
    conn = get_connection()
    cursor = conn.cursor()
    
    # Create scores table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS scores (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        quiz_type TEXT NOT NULL,
        player_name TEXT DEFAULT 'Anonymous',
        score INTEGER NOT NULL,
        total_questions INTEGER NOT NULL,
        percentage REAL NOT NULL,
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
    )
    ''')
    
    conn.commit()
    conn.close()

# Initialize the database when the module is imported
init_db() 