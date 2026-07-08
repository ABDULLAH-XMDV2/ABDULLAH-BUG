#!/usr/bin/env python3
# Configuration File
# Author: HeaNg[Black-Cyber]

import os

# ===== BOT CONFIGURATION =====
# Get token from environment variable (Railway/Render)
TOKEN = os.environ.get("BOT_TOKEN", "8945779411:AAE-JGLUItC0WPG9t_uXkKunhOtFDp-qdxE")

# Admin IDs - get from environment or set manually
ADMIN_IDS = [int(id) for id in os.environ.get("ADMIN_IDS", "6118251763").split(",")]

# ===== DATABASE =====
DB_FILE = os.environ.get("DB_FILE", "empire_bot.db")

# ===== ECONOMY SETTINGS =====
COINS_ON_JOIN = int(os.environ.get("COINS_ON_JOIN", "1"))
COST_PER_CRASH = int(os.environ.get("COST_PER_CRASH", "5"))
REFERRAL_BONUS = int(os.environ.get("REFERRAL_BONUS", "2"))
DAILY_BONUS = int(os.environ.get("DAILY_BONUS", "1"))

# ===== FILE PATHS =====
PAYLOAD_DIR = "payloads"
os.makedirs(PAYLOAD_DIR, exist_ok=True)

# ===== RAILWAY/RENDER SETTINGS =====
PORT = int(os.environ.get("PORT", 8080))
