#!/usr/bin/env python3
# Database Functions
# Author: HeaNg[Black-Cyber]

import sqlite3
import random
import string
from datetime import datetime
from config import DB_FILE, COINS_ON_JOIN, REFERRAL_BONUS

def init_db():
    """Initialize database with all tables"""
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    
    # Users table
    c.execute('''CREATE TABLE IF NOT EXISTS users (
        user_id INTEGER PRIMARY KEY,
        username TEXT,
        first_name TEXT,
        coins INTEGER DEFAULT 0,
        total_earned INTEGER DEFAULT 0,
        total_spent INTEGER DEFAULT 0,
        join_date TIMESTAMP,
        is_banned BOOLEAN DEFAULT 0,
        is_premium BOOLEAN DEFAULT 0,
        referred_by INTEGER,
        referral_code TEXT UNIQUE,
        daily_last_claim TIMESTAMP
    )''')
    
    # Transactions table
    c.execute('''CREATE TABLE IF NOT EXISTS transactions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        from_user INTEGER,
        to_user INTEGER,
        amount INTEGER,
        type TEXT,
        timestamp TIMESTAMP,
        description TEXT
    )''')
    
    # Coupons table
    c.execute('''CREATE TABLE IF NOT EXISTS coupons (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        code TEXT UNIQUE,
        amount INTEGER,
        used_by INTEGER,
        created_by INTEGER,
        created_at TIMESTAMP,
        used_at TIMESTAMP,
        is_used BOOLEAN DEFAULT 0
    )''')
    
    # Crashes table
    c.execute('''CREATE TABLE IF NOT EXISTS crashes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        target TEXT,
        payload_type TEXT,
        status TEXT,
        timestamp TIMESTAMP
    )''')
    
    # Shop items table
    c.execute('''CREATE TABLE IF NOT EXISTS shop_items (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        description TEXT,
        price INTEGER,
        type TEXT
    )''')
    
    conn.commit()
    conn.close()

def get_user(user_id):
    """Get user data from database"""
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("SELECT * FROM users WHERE user_id = ?", (user_id,))
    user = c.fetchone()
    conn.close()
    return user

def get_all_users():
    """Get all users"""
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("SELECT user_id, username, first_name, coins, is_banned FROM users ORDER BY coins DESC")
    users = c.fetchall()
    conn.close()
    return users

def create_user(user_id, username, first_name, referred_by=None):
    """Create new user"""
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    
    # Generate unique referral code
    ref_code = ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))
    
    # Check if user exists
    c.execute("SELECT user_id FROM users WHERE user_id = ?", (user_id,))
    if c.fetchone():
        conn.close()
        return False
    
    # Insert user
    c.execute('''INSERT INTO users 
        (user_id, username, first_name, coins, join_date, referral_code, referred_by, daily_last_claim)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)''',
        (user_id, username, first_name, COINS_ON_JOIN, datetime.now(), ref_code, referred_by, datetime.now()))
    
    # Give referral bonus
    if referred_by:
        c.execute("UPDATE users SET coins = coins + ? WHERE user_id = ?", (REFERRAL_BONUS, referred_by))
        c.execute('''INSERT INTO transactions 
            (from_user, to_user, amount, type, timestamp, description)
            VALUES (?, ?, ?, ?, ?, ?)''',
            (user_id, referred_by, REFERRAL_BONUS, 'referral', datetime.now(), f'Referral bonus from {user_id}'))
    
    conn.commit()
    conn.close()
    return True

def add_coins(user_id, amount, description="Coin addition"):
    """Add coins to user"""
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("UPDATE users SET coins = coins + ?, total_earned = total_earned + ? WHERE user_id = ?", 
              (amount, amount, user_id))
    c.execute('''INSERT INTO transactions 
        (from_user, to_user, amount, type, timestamp, description)
        VALUES (?, ?, ?, ?, ?, ?)''',
        (0, user_id, amount, 'earn', datetime.now(), description))
    conn.commit()
    conn.close()

def remove_coins(user_id, amount, description="Coin deduction"):
    """Remove coins from user"""
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("UPDATE users SET coins = coins - ?, total_spent = total_spent + ? WHERE user_id = ? AND coins >= ?", 
              (amount, amount, user_id, amount))
    if c.rowcount > 0:
        c.execute('''INSERT INTO transactions 
            (from_user, to_user, amount, type, timestamp, description)
            VALUES (?, ?, ?, ?, ?, ?)''',
            (user_id, 0, amount, 'spend', datetime.now(), description))
        conn.commit()
        conn.close()
        return True
    conn.close()
    return False

def generate_coupon(amount, created_by):
    """Generate a coupon code"""
    code = ''.join(random.choices(string.ascii_uppercase + string.digits, k=12))
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("INSERT INTO coupons (code, amount, created_by, created_at) VALUES (?, ?, ?, ?)",
              (code, amount, created_by, datetime.now()))
    conn.commit()
    conn.close()
    return code

def redeem_coupon(code, user_id):
    """Redeem a coupon"""
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("SELECT id, amount, is_used FROM coupons WHERE code = ?", (code,))
    coupon = c.fetchone()
    
    if not coupon:
        conn.close()
        return False, "Invalid coupon code"
    
    if coupon[2]:
        conn.close()
        return False, "Coupon already used"
    
    # Redeem coupon
    c.execute("UPDATE coupons SET used_by = ?, used_at = ?, is_used = 1 WHERE id = ?", 
              (user_id, datetime.now(), coupon[0]))
    add_coins(user_id, coupon[1], f"Coupon redemption: {code}")
    conn.commit()
    conn.close()
    return True, f"Successfully redeemed {coupon[1]} coins!"

def log_crash(user_id, target, payload_type):
    """Log a crash attack"""
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("INSERT INTO crashes (user_id, target, payload_type, status, timestamp) VALUES (?, ?, ?, ?, ?)",
              (user_id, target, payload_type, 'generated', datetime.now()))
    conn.commit()
    conn.close()

def get_crash_stats():
    """Get crash statistics"""
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("SELECT COUNT(*) FROM crashes")
    total = c.fetchone()[0]
    c.execute("SELECT payload_type, COUNT(*) FROM crashes GROUP BY payload_type")
    types = c.fetchall()
    conn.close()
    return total, types

def can_claim_daily(user_id):
    """Check if user can claim daily bonus"""
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("SELECT daily_last_claim FROM users WHERE user_id = ?", (user_id,))
    result = c.fetchone()
    conn.close()
    
    if not result:
        return True
    
    last_claim = datetime.fromisoformat(result[0])
    now = datetime.now()
    return (now - last_claim).days >= 1

def update_daily_claim(user_id):
    """Update daily claim timestamp"""
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("UPDATE users SET daily_last_claim = ? WHERE user_id = ?", (datetime.now(), user_id))
    conn.commit()
    conn.close()