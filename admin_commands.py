#!/usr/bin/env python3
# Admin Commands
# Author: HeaNg[Black-Cyber]

import os
import sqlite3
from telegram import Update, ParseMode
from telegram.ext import ContextTypes

from config import ADMIN_IDS, DB_FILE
from database import get_all_users, generate_coupon, add_coins, get_crash_stats
from buttons import ModernButtons

async def admin_panel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Admin panel"""
    user_id = update.effective_user.id
    
    if user_id not in ADMIN_IDS:
        await update.message.reply_text("🚫 You don't have permission to use this command!")
        return
    
    reply_markup = ModernButtons.admin_panel()
    
    await update.message.reply_text(
        "⚙️ **𝗔𝗗𝗠𝗜𝗡 𝗣𝗔𝗡𝗘𝗟** ⚙️\n"
        "Select an option below:",
        reply_markup=reply_markup,
        parse_mode='Markdown'
    )

async def admin_users(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Show all users"""
    user_id = update.effective_user.id
    
    if user_id not in ADMIN_IDS:
        await update.message.reply_text("🚫 Access denied!")
        return
    
    users = get_all_users()
    
    if not users:
        await update.message.reply_text("📋 No users found.")
        return
    
    msg = "👥 **𝗨𝗦𝗘𝗥 𝗟𝗜𝗦𝗧** (Top 50)\n\n"
    for user_id, username, first_name, coins, is_banned in users[:50]:
        name = username or first_name or str(user_id)
        status = "🚫" if is_banned else "✅"
        msg += f"{status} **{name}** - {coins} coins (ID: {user_id})\n"
    
    await update.message.reply_text(msg[:4000], parse_mode='Markdown')

async def admin_create_coupon(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Create coupon (admin only)"""
    user_id = update.effective_user.id
    
    if user_id not in ADMIN_IDS:
        await update.message.reply_text("🚫 Access denied!")
        return
    
    args = context.args
    if len(args) < 1:
        await update.message.reply_text("❌ Usage: /createcoupon <amount>\nExample: /createcoupon 100")
        return
    
    amount = int(args[0]) if args[0].isdigit() else 0
    if amount <= 0:
        await update.message.reply_text("❌ Amount must be positive!")
        return
    
    code = generate_coupon(amount, user_id)
    await update.message.reply_text(
        f"✅ **Coupon Created!**\n"
        f"🎫 Code: `{code}`\n"
        f"💰 Amount: {amount} coins\n"
        f"🔗 Share: /coupon {code}",
        parse_mode='Markdown'
    )

async def admin_ban(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Ban user (admin only)"""
    user_id = update.effective_user.id
    
    if user_id not in ADMIN_IDS:
        await update.message.reply_text("🚫 Access denied!")
        return
    
    args = context.args
    if len(args) < 1:
        await update.message.reply_text("❌ Usage: /ban <user_id or @username>")
        return
    
    target = args[0]
    target_id = None
    
    if target.startswith('@'):
        conn = sqlite3.connect(DB_FILE)
        c = conn.cursor()
        c.execute("SELECT user_id FROM users WHERE username = ?", (target[1:],))
        result = c.fetchone()
        conn.close()
        if result:
            target_id = result[0]
    elif target.isdigit():
        target_id = int(target)
    
    if not target_id:
        await update.message.reply_text("❌ User not found!")
        return
    
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("UPDATE users SET is_banned = 1 WHERE user_id = ?", (target_id,))
    conn.commit()
    conn.close()
    
    await update.message.reply_text(f"✅ User {target} has been banned!")

async def admin_unban(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Unban user (admin only)"""
    user_id = update.effective_user.id
    
    if user_id not in ADMIN_IDS:
        await update.message.reply_text("🚫 Access denied!")
        return
    
    args = context.args
    if len(args) < 1:
        await update.message.reply_text("❌ Usage: /unban <user_id or @username>")
        return
    
    target = args[0]
    target_id = None
    
    if target.startswith('@'):
        conn = sqlite3.connect(DB_FILE)
        c = conn.cursor()
        c.execute("SELECT user_id FROM users WHERE username = ?", (target[1:],))
        result = c.fetchone()
        conn.close()
        if result:
            target_id = result[0]
    elif target.isdigit():
        target_id = int(target)
    
    if not target_id:
        await update.message.reply_text("❌ User not found!")
        return
    
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("UPDATE users SET is_banned = 0 WHERE user_id = ?", (target_id,))
    conn.commit()
    conn.close()
    
    await update.message.reply_text(f"✅ User {target} has been unbanned!")

async def admin_give(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Give coins to user (admin only)"""
    user_id = update.effective_user.id
    
    if user_id not in ADMIN_IDS:
        await update.message.reply_text("🚫 Access denied!")
        return
    
    args = context.args
    if len(args) < 2:
        await update.message.reply_text("❌ Usage: /givecoins <user_id or @username> <amount>")
        return
    
    target = args[0]
    amount = int(args[1]) if args[1].isdigit() else 0
    
    if amount <= 0:
        await update.message.reply_text("❌ Amount must be positive!")
        return
    
    target_id = None
    if target.startswith('@'):
        conn = sqlite3.connect(DB_FILE)
        c = conn.cursor()
        c.execute("SELECT user_id FROM users WHERE username = ?", (target[1:],))
        result = c.fetchone()
        conn.close()
        if result:
            target_id = result[0]
    elif target.isdigit():
        target_id = int(target)
    
    if not target_id:
        await update.message.reply_text("❌ User not found!")
        return
    
    add_coins(target_id, amount, f"Admin gift from {user_id}")
    await update.message.reply_text(f"✅ Added {amount} coins to {target}!")

async def admin_stats(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Show full statistics (admin only)"""
    user_id = update.effective_user.id
    
    if user_id not in ADMIN_IDS:
        await update.message.reply_text("🚫 Access denied!")
        return
    
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    
    c.execute("SELECT COUNT(*) FROM users")
    total_users = c.fetchone()[0]
    
    c.execute("SELECT SUM(coins) FROM users")
    total_coins = c.fetchone()[0] or 0
    
    c.execute("SELECT COUNT(*) FROM users WHERE is_banned = 1")
    banned_users = c.fetchone()[0]
    
    c.execute("SELECT COUNT(*) FROM crashes")
    total_crashes = c.fetchone()[0]
    
    c.execute("SELECT COUNT(*) FROM transactions")
    total_transactions = c.fetchone()[0]
    
    c.execute("SELECT COUNT(*) FROM coupons WHERE is_used = 0")
    unused_coupons = c.fetchone()[0]
    
    conn.close()
    
    msg = f"""
📊 **𝗙𝗨𝗟𝗟 𝗦𝗧𝗔𝗧𝗜𝗦𝗧𝗜𝗖𝗦**
─────────────────────
👥 Total Users: {total_users}
💰 Total Coins: {total_coins}
🚫 Banned Users: {banned_users}
💀 Total Crashes: {total_crashes}
📝 Transactions: {total_transactions}
🎫 Unused Coupons: {unused_coupons}

💡 **Admin Actions:**
• /createcoupon <amount> - Create coupon
• /ban <user> - Ban user
• /unban <user> - Unban user
• /givecoins <user> <amount> - Give coins
"""
    await update.message.reply_text(msg, parse_mode='Markdown')

async def admin_crashes(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Show crash logs (admin only)"""
    user_id = update.effective_user.id
    
    if user_id not in ADMIN_IDS:
        await update.message.reply_text("🚫 Access denied!")
        return
    
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("SELECT id, user_id, target, payload_type, status, timestamp FROM crashes ORDER BY timestamp DESC LIMIT 20")
    crashes = c.fetchall()
    conn.close()
    
    if not crashes:
        await update.message.reply_text("📋 No crashes found.")
        return
    
    msg = "💀 **𝗖𝗥𝗔𝗦𝗛 𝗟𝗢𝗚𝗦** (Last 20)\n\n"
    for crash_id, user_id, target, payload_type, status, timestamp in crashes:
        msg += f"🕐 {timestamp[:19]}\n"
        msg += f"👤 User: {user_id}\n"
        msg += f"📱 Target: {target}\n"
        msg += f"💀 Type: {payload_type}\n"
        msg += f"📊 Status: {status}\n\n"
    
    await update.message.reply_text(msg[:4000], parse_mode='Markdown')

async def admin_clear(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Clear database (admin only)"""
    user_id = update.effective_user.id
    
    if user_id not in ADMIN_IDS:
        await update.message.reply_text("🚫 Access denied!")
        return
    
    # Confirm first
    await update.message.reply_text(
        "⚠️ **WARNING!** This will delete ALL data!\n"
        "Type `/confirm_clear` to confirm."
    )

async def confirm_clear(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Confirm clear database"""
    user_id = update.effective_user.id
    
    if user_id not in ADMIN_IDS:
        await update.message.reply_text("🚫 Access denied!")
        return
    
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    
    # Delete all data
    c.execute("DELETE FROM users")
    c.execute("DELETE FROM transactions")
    c.execute("DELETE FROM coupons")
    c.execute("DELETE FROM crashes")
    
    conn.commit()
    conn.close()
    
    await update.message.reply_text("✅ Database cleared successfully!")