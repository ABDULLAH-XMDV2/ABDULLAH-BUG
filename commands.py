#!/usr/bin/env python3
# User Commands
# Author: HeaNg[Black-Cyber]

import os
import time
from datetime import datetime
from telegram import Update, ParseMode
from telegram.ext import ContextTypes

from config import ADMIN_IDS, COST_PER_CRASH, COINS_ON_JOIN, REFERRAL_BONUS, PAYLOAD_DIR
from database import (
    get_user, create_user, add_coins, remove_coins, 
    redeem_coupon, log_crash, can_claim_daily, update_daily_claim
)
from payloads import generate_payload
from buttons import ModernButtons

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Start command with welcome message"""
    user = update.effective_user
    user_id = user.id
    
    # Check if user exists
    existing = get_user(user_id)
    if not existing:
        # Check for referral
        ref_code = context.args[0] if context.args else None
        referred_by = None
        if ref_code:
            conn = sqlite3.connect(DB_FILE)
            c = conn.cursor()
            c.execute("SELECT user_id FROM users WHERE referral_code = ?", (ref_code,))
            result = c.fetchone()
            conn.close()
            if result:
                referred_by = result[0]
        
        create_user(user_id, user.username, user.first_name, referred_by)
        coins = COINS_ON_JOIN
    else:
        coins = existing[3]
    
    reply_markup = ModernButtons.main_menu()
    
    welcome_msg = f"""
🔥 **𝗪𝗘𝗟𝗖𝗢𝗠𝗘 𝗧𝗢 𝗧𝗛𝗘 𝗖𝗥𝗔𝗦𝗛 𝗘𝗠𝗣𝗜𝗥𝗘** 🔥

👋 Hello {user.first_name}!
💰 Your balance: **{coins} coins**

💀 **What can you do?**
• Crash WhatsApp users (5 coins per crash)
• Earn coins by inviting friends
• Redeem coupon codes
• Buy premium features
• Claim daily bonus

📌 **Commands:**
/balance - Check your coins
/attack <phone> <type> - Crash someone
/referral - Get your referral link
/coupon <code> - Redeem a coupon
/send <user> <amount> - Send coins
/leaderboard - Top coin holders
/daily - Claim daily bonus
/help - Show all commands
"""
    await update.message.reply_text(welcome_msg, reply_markup=reply_markup, parse_mode='Markdown')

async def balance(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Check user balance"""
    user_id = update.effective_user.id
    user = get_user(user_id)
    
    if not user:
        await update.message.reply_text("❌ You need to /start first!")
        return
    
    coins = user[3]
    total_earned = user[4]
    total_spent = user[5]
    is_premium = user[8]
    
    msg = f"""
💰 **𝗬𝗢𝗨𝗥 𝗕𝗔𝗟𝗔𝗡𝗖𝗘**
─────────────────────
🪙 Coins: **{coins}**
📈 Total Earned: **{total_earned}**
📉 Total Spent: **{total_spent}**
⭐ Premium: **{'✅ Yes' if is_premium else '❌ No'}**

💀 **Crash Cost:** 5 coins per attack
💡 **Earn coins:** Invite friends or use coupons!
🎁 **Daily Bonus:** 1 coin (use /daily)
"""
    await update.message.reply_text(msg, parse_mode='Markdown')

async def daily(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Claim daily bonus"""
    user_id = update.effective_user.id
    user = get_user(user_id)
    
    if not user:
        await update.message.reply_text("❌ You need to /start first!")
        return
    
    if can_claim_daily(user_id):
        add_coins(user_id, 1, "Daily bonus")
        update_daily_claim(user_id)
        await update.message.reply_text("🎁 **Daily bonus claimed!**\n💰 +1 coin added to your balance!")
    else:
        await update.message.reply_text("⏳ You already claimed your daily bonus!\nCome back tomorrow for more!")

async def referral(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Get referral link"""
    user_id = update.effective_user.id
    user = get_user(user_id)
    
    if not user:
        await update.message.reply_text("❌ You need to /start first!")
        return
    
    ref_code = user[9]
    bot_name = context.bot.username
    
    msg = f"""
👑 **𝗥𝗘𝗙𝗘𝗥𝗥𝗔𝗟 𝗣𝗥𝗢𝗚𝗥𝗔𝗠**
─────────────────────
💰 You earn **{REFERRAL_BONUS} coins** for each friend who joins!
🎁 Your friend also gets **{COINS_ON_JOIN} coins**!

🔗 **Your referral link:**
`https://t.me/{bot_name}?start={ref_code}`

📊 **Your stats:**
• Total referrals: (coming soon)
• Coins earned: {user[4]}

💡 Share your link and earn unlimited coins!
"""
    await update.message.reply_text(msg, parse_mode='Markdown')

async def coupon(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Redeem coupon code"""
    user_id = update.effective_user.id
    
    if not get_user(user_id):
        await update.message.reply_text("❌ You need to /start first!")
        return
    
    args = context.args
    if not args:
        await update.message.reply_text("❌ Usage: /coupon <code>\nExample: /coupon ABC123XYZ")
        return
    
    code = args[0].upper()
    success, message = redeem_coupon(code, user_id)
    
    if success:
        await update.message.reply_text(f"✅ {message}\n💰 New balance: {get_user(user_id)[3]}")
    else:
        await update.message.reply_text(f"❌ {message}")

async def send_coins(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Send coins to another user"""
    user_id = update.effective_user.id
    user = get_user(user_id)
    
    if not user:
        await update.message.reply_text("❌ You need to /start first!")
        return
    
    args = context.args
    if len(args) < 2:
        await update.message.reply_text("❌ Usage: /send <@username or user_id> <amount>")
        return
    
    target = args[0]
    amount = int(args[1]) if args[1].isdigit() else 0
    
    if amount <= 0:
        await update.message.reply_text("❌ Amount must be positive!")
        return
    
    if user[3] < amount:
        await update.message.reply_text(f"❌ Not enough coins! You have {user[3]} coins.")
        return
    
    # Find target user
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
    
    if target_id == user_id:
        await update.message.reply_text("❌ You can't send coins to yourself!")
        return
    
    # Transfer coins
    if remove_coins(user_id, amount, f"Transfer to {target_id}"):
        add_coins(target_id, amount, f"Transfer from {user_id}")
        await update.message.reply_text(f"✅ Sent {amount} coins to {target}!\n💰 Your new balance: {get_user(user_id)[3]}")
    else:
        await update.message.reply_text("❌ Transfer failed!")

async def leaderboard(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Show top coin holders"""
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("SELECT user_id, username, coins FROM users ORDER BY coins DESC LIMIT 10")
    top_users = c.fetchall()
    conn.close()
    
    if not top_users:
        await update.message.reply_text("📊 No users yet!")
        return
    
    msg = "🏆 **𝗟𝗘𝗔𝗗𝗘𝗥𝗕𝗢𝗔𝗥𝗗** 🏆\n\n"
    for i, (user_id, username, coins) in enumerate(top_users, 1):
        name = username or f"User {user_id}"
        medal = get_medal(i)
        msg += f"{medal} **{name}** - {coins} coins\n"
    
    await update.message.reply_text(msg, parse_mode='Markdown')

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Show help message"""
    msg = """
📚 **𝗛𝗘𝗟𝗣 𝗠𝗘𝗡𝗨**

**💰 Economy Commands:**
/balance - Check your coins
/daily - Claim daily bonus
/send <user> <amount> - Send coins
/leaderboard - Top coin holders

**💀 Attack Commands:**
/attack <phone> <type> - Crash someone
• Types: text, vcard, location, media
• Cost: 5 coins per attack

**👑 Referral Commands:**
/referral - Get your referral link
/coupon <code> - Redeem a coupon

**⚙️ Other Commands:**
/start - Main menu
/help - This message
/shop - View shop items
/settings - Bot settings

**💡 Tips:**
• Invite friends to earn coins
• Claim daily bonus every day
• Use coupons for free coins
• Buy premium for discounts
"""
    await update.message.reply_text(msg, parse_mode='Markdown')