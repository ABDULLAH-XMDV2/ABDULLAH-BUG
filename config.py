#!/usr/bin/env python3
# Configuration File
# Author: HeaNg[Black-Cyber]

import os

# ===== BOT CONFIGURATION =====
TOKEN = "YOUR_BOT_TOKEN_HERE"
ADMIN_IDS = [123456789, 987654321]  # List of admin IDs

# ===== DATABASE =====
DB_FILE = "empire_bot.db"

# ===== ECONOMY SETTINGS =====
COINS_ON_JOIN = 1
COST_PER_CRASH = 5
REFERRAL_BONUS = 2
DAILY_BONUS = 1

# ===== FILE PATHS =====
PAYLOAD_DIR = "payloads"
os.makedirs(PAYLOAD_DIR, exist_ok=True)