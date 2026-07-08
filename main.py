#!/usr/bin/env python3
# WhatsApp Crash Empire - Main Entry Point
# Author: HeaNg[Black-Cyber]
# Version: 3.0 - Ultimate Pro Edition - Railway Fix

import logging
import os
import sys
from telegram import Update
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

# Add current directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from config import TOKEN
from database import init_db
from commands import (
    start, balance, daily, referral, coupon, 
    send_coins, leaderboard, help_command
)
from admin_commands import (
    admin_panel, admin_users, admin_create_coupon,
    admin_ban, admin_unban, admin_give, admin_stats,
    admin_crashes, admin_clear, confirm_clear
)
from handlers import button_callback
from attack import attack_command

# ===== SETUP LOGGING =====
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

def main():
    """Start the bot"""
    try:
        # Initialize database
        init_db()
        logger.info("✅ Database initialized")
        
        # Check token
        if not TOKEN or TOKEN == "YOUR_BOT_TOKEN_HERE":
            logger.error("❌ Please set your bot token in config.py!")
            print("❌ ERROR: Bot token not configured!")
            print("Please edit config.py and add your bot token.")
            sys.exit(1)
        
        # Create application
        app = Application.builder().token(TOKEN).build()
        
        # ===== USER COMMANDS =====
        app.add_handler(CommandHandler("start", start))
        app.add_handler(CommandHandler("help", help_command))
        app.add_handler(CommandHandler("balance", balance))
        app.add_handler(CommandHandler("daily", daily))
        app.add_handler(CommandHandler("referral", referral))
        app.add_handler(CommandHandler("coupon", coupon))
        app.add_handler(CommandHandler("send", send_coins))
        app.add_handler(CommandHandler("leaderboard", leaderboard))
        app.add_handler(CommandHandler("attack", attack_command))
        
        # ===== ADMIN COMMANDS =====
        app.add_handler(CommandHandler("admin", admin_panel))
        app.add_handler(CommandHandler("users", admin_users))
        app.add_handler(CommandHandler("createcoupon", admin_create_coupon))
        app.add_handler(CommandHandler("ban", admin_ban))
        app.add_handler(CommandHandler("unban", admin_unban))
        app.add_handler(CommandHandler("givecoins", admin_give))
        app.add_handler(CommandHandler("stats", admin_stats))
        app.add_handler(CommandHandler("crashes", admin_crashes))
        app.add_handler(CommandHandler("clear", admin_clear))
        app.add_handler(CommandHandler("confirm_clear", confirm_clear))
        
        # ===== BUTTON HANDLER =====
        app.add_handler(CallbackQueryHandler(button_callback))
        
        # ===== START BOT =====
        logger.info("🚀 Bot started successfully!")
        print("🔥 WhatsApp Crash Empire - Ultimate Pro Bot")
        print("💀 Ready to destroy some WhatsApp clients!")
        print("👑 Admin commands available")
        print("🤖 Bot is running...")
        
        # Start polling with error handling
        app.run_polling(allowed_updates=Update.ALL_TYPES)
        
    except Exception as e:
        logger.error(f"❌ Bot crashed: {e}")
        print(f"❌ ERROR: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()