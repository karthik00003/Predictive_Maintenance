#!/usr/bin/env python3
"""
Create test users in the database
"""

import sqlite3

conn = sqlite3.connect("users.db")
cursor = conn.cursor()

# Add test user
try:
    cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", 
                   ("testuser", "password123"))
    conn.commit()
    print("Test user created successfully!")
except sqlite3.IntegrityError:
    print("Test user already exists")
finally:
    conn.close()
