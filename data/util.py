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
        await db.commit()


async def init_sample_data():
    """Initialize the database with sample customer data."""
    async with await get_database() as db:
        # Check if data already exists
        cursor = await db.execute("SELECT COUNT(*) FROM customers")
        count = (await cursor.fetchone())[0]
        
        if count == 0:
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
            
            await db.commit()


async def close_database():
    """Close database connections (for cleanup)."""
    # aiosqlite handles connection cleanup automatically
    pass