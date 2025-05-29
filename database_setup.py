import sqlite3
import os
from datetime import datetime

def init_db():
    """Initialize the database with all required tables"""
    db_path = 'kishanx.db'
    
    # Create database if it doesn't exist
    if not os.path.exists(db_path):
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Create users table
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            registered_at TEXT NOT NULL,
            last_login TEXT,
            balance REAL DEFAULT 10000.0,
            is_premium BOOLEAN DEFAULT 0
        )
        ''')
        
        # Create trades table
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS trades (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            symbol TEXT NOT NULL,
            direction TEXT NOT NULL,
            entry_price REAL NOT NULL,
            exit_price REAL,
            quantity REAL NOT NULL,
            status TEXT NOT NULL,
            entry_time TEXT NOT NULL,
            exit_time TEXT,
            profit_loss REAL,
            stop_loss REAL,
            take_profit REAL,
            FOREIGN KEY (user_id) REFERENCES users (id)
        )
        ''')
        
        # Create market_data table
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS market_data (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            symbol TEXT NOT NULL,
            price REAL NOT NULL,
            volume REAL,
            timestamp TEXT NOT NULL
        )
        ''')
        
        # Create signals table
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS signals (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            pair TEXT NOT NULL,
            direction TEXT NOT NULL,
            confidence REAL NOT NULL,
            created_at TEXT NOT NULL,
            FOREIGN KEY (user_id) REFERENCES users (id)
        )
        ''')
        
        # Create positions table
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS positions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            symbol TEXT NOT NULL,
            quantity REAL NOT NULL,
            average_price REAL NOT NULL,
            last_updated TEXT NOT NULL,
            FOREIGN KEY (user_id) REFERENCES users (id),
            UNIQUE(user_id, symbol)
        )
        ''')
        
        # Create risk_limits table
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS risk_limits (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            max_position_size REAL DEFAULT 0.02,
            max_daily_loss REAL DEFAULT 0.05,
            max_drawdown REAL DEFAULT 0.15,
            stop_loss_pct REAL DEFAULT 0.02,
            take_profit_pct REAL DEFAULT 0.04,
            updated_at TEXT NOT NULL,
            FOREIGN KEY (user_id) REFERENCES users (id)
        )
        ''')
        
        # Create portfolio_history table
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS portfolio_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            portfolio_value REAL NOT NULL,
            timestamp TEXT NOT NULL,
            FOREIGN KEY (user_id) REFERENCES users (id)
        )
        ''')
        
        conn.commit()
        conn.close()
        print("Database initialized successfully!")
    else:
        print("Database already exists.")

if __name__ == "__main__":
    init_db() 