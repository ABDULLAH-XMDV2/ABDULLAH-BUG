#!/usr/bin/env python3
# Callback Handlers
# Author: HeaNg[Black-Cyber]

import os
from telegram import Update
from telegram.ext import ContextTypes

from config import ADMIN_IDS
from database import get_user, add_coins, remove_coins, log_crash
from payloads import generate_payload
from buttons import ModernButtons

async def button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle all button callbacks"""
    query = update.callback_query
    await query.answer()
    
    user_id = update.effective_user.id
    data = query.data
    
    # Main menu navigation
    if data == "main_menu":
        reply_markup = ModernButtons.main_menu()
        await query.edit_message_text(
            "🏠 **Main Menu**\nSelect an option:",
            reply_markup=reply_markup,
            parse_mode='Markdown'
        )
        return
    
    if data == "attack_menu":
        reply_markup = ModernButtons.attack_menu()
        await query.edit_message_text(
            "💀 **Attack Menu**\nSelect attack type:",
            reply_markup=reply_markup,
            parse_mode='Markdown'
        )
        return
    
    if data == "shop":
        reply_markup = ModernButtons.shop_menu()
        await query.edit_message_text(
            "🏪 **Shop**\nBuy items with your coins:",
            reply_markup=reply_markup,
            parse_mode='Markdown'
        )
        return
    
    if data == "settings":
        reply_markup = ModernButtons.settings_menu()
        await query.edit_message_text(
            "⚙️ **Settings**\nConfigure your bot:",
            reply_markup=reply_markup,
            parse_mode='Markdown'
        )
        return
    
    # Admin panel
    if data == "admin_panel":
        if user_id not in ADMIN_IDS:
            await query.edit_message_text("🚫 Access denied!")
            return
        reply_markup = ModernButtons.admin_panel()
        await query.edit_message_text(
            "⚙️ **Admin Panel**",
            reply_markup=reply_markup,
            parse_mode='Markdown'
        )
        return
    
    # Attack types
    if data.startswith("attack_"):
        attack_type = data.replace("attack_", "")
        await query.edit_message_text(
            f"💀 **Attack: {attack_type.upper()}**\n\n"
            f"Use: /attack <phone> {attack_type}\n"
            f"Example: /attack 1234567890 {attack_type}\n\n"
            f"💰 Cost: 5 coins",
            parse_mode='Markdown'
        )
        return
    
    # Admin actions
    if data == "admin_users":
        from admin_commands import admin_users
        await admin_users(update, context)
        return
    
    if data == "admin_coupon":
        await query.edit_message_text(
            "🎫 **Create Coupon**\n\n"
            "Use: /createcoupon <amount>\n"
            "Example: /createcoupon 100",
            parse_mode='Markdown'
        )
        return
    
    if data == "admin_ban":
        await query.edit_message_text(
            "🚫 **Ban User**\n\n"
            "Use: /ban <user_id or @username>\n"
            "Example: /ban @username",
            parse_mode='Markdown'
        )
        return
    
    if data == "admin_unban":
        await query.edit_message_text(
            "✅ **Unban User**\n\n"
            "Use: /unban <user_id or @username>\n"
            "Example: /unban @username",
            parse_mode='Markdown'
        )
        return
    
    if data == "admin_give":
        await query.edit_message_text(
            "💰 **Give Coins**\n\n"
            "Use: /givecoins <user_id or @username> <amount>\n"
            "Example: /givecoins @username 100",
            parse_mode='Markdown'
        )
        return
    
    if data == "admin_stats":
        from admin_commands import admin_stats
        await admin_stats(update, context)
        return
    
    if data == "admin_crashes":
        from admin_commands import admin_crashes
        await admin_crashes(update, context)
        return
    
    if data == "admin_clear":
        from admin_commands import admin_clear
        await admin_clear(update, context)
        return
    
    # Balance
    if data == "balance":
        from commands import balance
        await balance(update, context)
        return
    
    # Referral
    if data == "referral":
        from commands import referral
        await referral(update, context)
        return
    
    # Stats
    if data == "stats":
        from commands import leaderboard
        await leaderboard(update, context)
        return
    
    # Coupon
    if data == "coupon":
        await query.edit_message_text(
            "🎫 **Redeem Coupon**\n\n"
            "Use: /coupon <code>\n"
            "Example: /coupon ABC123XYZ",
            parse_mode='Markdown'
        )
        return
    
    # Daily bonus
    if data == "daily":
        from commands import daily
        await daily(update, context)
        return
    
    # Help
    if data == "help":
        from commands import help_command
        await help_command(update, context)
        return
    
    # Shop items
    if data.startswith("shop_"):
        item = data.replace("shop_", "")
        user = get_user(user_id)
        
        if not user:
            await query.edit_message_text("❌ Please /start first!")
            return
        
        prices = {
            "premium": 50,
            "crashpack": 25,
            "bonus": 10,
            "protect": 30
        }
        
        if item in prices:
            price = prices[item]
            if user[3] >= price:
                remove_coins(user_id, price, f"Shop purchase: {item}")
                await query.edit_message_text(
                    f"✅ **Purchase Successful!**\n\n"
                    f"Item: {item.upper()}\n"
                    f"💰 Cost: {price} coins\n"
                    f"🪙 New balance: {get_user(user_id)[3]}\n\n"
                    f"Thank you for your purchase!",
                    parse_mode='Markdown'
                )
            else:
                await query.edit_message_text(
                    f"❌ **Not enough coins!**\n\n"
                    f"Item: {item.upper()}\n"
                    f"💰 Cost: {price} coins\n"
                    f"🪙 Your balance: {user[3]}\n"
                    f"Need {price - user[3]} more coins!",
                    parse_mode='Markdown'
                )
        return
    
    # Default response
    await query.edit_message_text("❌ Unknown option!")