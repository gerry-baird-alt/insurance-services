import aiosqlite
import os
from typing import Optional

DATABASE_PATH = "insurance.db"


async def get_database() -> aiosqlite.Connection:
    """Get database connection."""
    return aiosqlite.connect(DATABASE_PATH)


async def init_database():
    """Initialize the database with required tables."""
    async with await get_database() as db:
        await db.execute("""
            CREATE TABLE IF NOT EXISTS customers (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                date_of_birth TEXT NOT NULL,
                email TEXT UNIQUE NOT NULL,
                address TEXT NOT NULL,
                state TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        await db.execute("""
            CREATE TABLE IF NOT EXISTS policies (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                customer_id INTEGER NOT NULL,
                start_date TEXT NOT NULL,
                end_date TEXT NOT NULL,
                product TEXT NOT NULL,
                premium TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (customer_id) REFERENCES customers (id)
            )
        """)
        await db.commit()


async def init_sample_data():
    """Always reinitialize the database with fresh sample customer and policy data."""
    async with await get_database() as db:
        # Clear existing data
        await db.execute("DELETE FROM policies")
        await db.execute("DELETE FROM customers")
        
        # Reset auto-increment counters
        await db.execute("DELETE FROM sqlite_sequence WHERE name IN ('customers', 'policies')")
        
        # Insert sample customers
        sample_customers = [
            ("John Smith", "1985-06-15", "john.smith@email.com", "123 Main St", "California"),
            ("Sarah Johnson", "1990-03-22", "sarah.johnson@email.com", "456 Oak Ave", "Texas"),
            ("Michael Brown", "1978-11-08", "michael.brown@email.com", "789 Pine Rd", "New York"),
            ("Emily Davis", "1995-01-30", "emily.davis@email.com", "321 Elm St", "Florida"),
            ("David Wilson", "1982-09-12", "david.wilson@email.com", "654 Maple Dr", "Illinois")
        ]
        
        await db.executemany("""
            INSERT INTO customers (name, date_of_birth, email, address, state)
            VALUES (?, ?, ?, ?, ?)
        """, sample_customers)
        
        # Insert sample policies
        sample_policies = [
            (1, "2024-01-15", "2025-01-15", "bicycle", "450.00"),
            (1, "2024-03-01", "2025-03-01", "pet", "320.00"),
            (2, "2024-02-10", "2025-02-10", "boat", "1250.00"),
            (2, "2024-06-01", "2025-06-01", "RV", "2100.00"),
            (3, "2024-01-01", "2025-01-01", "equine", "890.00"),
            (3, "2024-04-15", "2025-04-15", "bicycle", "380.00"),
            (4, "2024-05-20", "2025-05-20", "pet", "295.00"),
            (5, "2024-07-01", "2025-07-01", "boat", "1450.00"),
            (5, "2024-08-15", "2025-08-15", "equine", "950.00")
        ]
        
        await db.executemany("""
            INSERT INTO policies (customer_id, start_date, end_date, product, premium)
            VALUES (?, ?, ?, ?, ?)
        """, sample_policies)
        
        await db.commit()


async def close_database():
    """Close database connections (for cleanup)."""
    # aiosqlite handles connection cleanup automatically
    pass