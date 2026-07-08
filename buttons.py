#!/usr/bin/env python3
# Modern UI Buttons
# Author: HeaNg[Black-Cyber]

from telegram import InlineKeyboardButton, InlineKeyboardMarkup

class ModernButtons:
    """🔥 Modern UI Button System - 2026 Style"""
    
    @staticmethod
    def main_menu():
        """🏠 Main Menu - Clean & Professional"""
        keyboard = [
            [
                InlineKeyboardButton("💰 𝗕𝗔𝗟𝗔𝗡𝗖𝗘", callback_data="balance"),
                InlineKeyboardButton("💀 𝗔𝗧𝗧𝗔𝗖𝗞", callback_data="attack_menu")
            ],
            [
                InlineKeyboardButton("👑 𝗥𝗘𝗙𝗘𝗥𝗥𝗔𝗟", callback_data="referral"),
                InlineKeyboardButton("🏪 𝗦𝗛𝗢𝗣", callback_data="shop")
            ],
            [
                InlineKeyboardButton("📊 𝗦𝗧𝗔𝗧𝗦", callback_data="stats"),
                InlineKeyboardButton("⚙️ 𝗦𝗘𝗧𝗧𝗜𝗡𝗚𝗦", callback_data="settings")
            ],
            [
                InlineKeyboardButton("🎫 𝗖𝗢𝗨𝗣𝗢𝗡", callback_data="coupon"),
                InlineKeyboardButton("🏆 𝗟𝗘𝗔𝗗𝗘𝗥𝗕𝗢𝗔𝗥𝗗", callback_data="leaderboard")
            ],
            [
                InlineKeyboardButton("🎁 𝗗𝗔𝗜𝗟𝗬 𝗕𝗢𝗡𝗨𝗦", callback_data="daily"),
                InlineKeyboardButton("❓ 𝗛𝗘𝗟𝗣", callback_data="help")
            ]
        ]
        return InlineKeyboardMarkup(keyboard)
    
    @staticmethod
    def attack_menu():
        """💀 Attack Menu - Dark Mode Style"""
        keyboard = [
            [
                InlineKeyboardButton("📝 𝗧𝗘𝗫𝗧 𝗕𝗢𝗠𝗕", callback_data="attack_text"),
                InlineKeyboardButton("📇 𝗩𝗖𝗔𝗥𝗗", callback_data="attack_vcard")
            ],
            [
                InlineKeyboardButton("📍 𝗟𝗢𝗖𝗔𝗧𝗜𝗢𝗡", callback_data="attack_location"),
                InlineKeyboardButton("🎬 𝗠𝗘𝗗𝗜𝗔", callback_data="attack_media")
            ],
            [
                InlineKeyboardButton("💀 𝗖𝗨𝗦𝗧𝗢𝗠", callback_data="attack_custom"),
                InlineKeyboardButton("📚 𝗛𝗢𝗪 𝗧𝗢", callback_data="attack_howto")
            ],
            [
                InlineKeyboardButton("◀️ 𝗕𝗔𝗖𝗞", callback_data="main_menu")
            ]
        ]
        return InlineKeyboardMarkup(keyboard)
    
    @staticmethod
    def admin_panel():
        """⚙️ Admin Panel - Full Control"""
        keyboard = [
            [
                InlineKeyboardButton("👥 𝗨𝗦𝗘𝗥𝗦", callback_data="admin_users"),
                InlineKeyboardButton("🎫 𝗖𝗢𝗨𝗣𝗢𝗡", callback_data="admin_coupon")
            ],
            [
                InlineKeyboardButton("🚫 𝗕𝗔𝗡", callback_data="admin_ban"),
                InlineKeyboardButton("✅ 𝗨𝗡𝗕𝗔𝗡", callback_data="admin_unban")
            ],
            [
                InlineKeyboardButton("💰 𝗚𝗜𝗩𝗘", callback_data="admin_give"),
                InlineKeyboardButton("📊 𝗦𝗧𝗔𝗧𝗦", callback_data="admin_stats")
            ],
            [
                InlineKeyboardButton("💀 𝗖𝗥𝗔𝗦𝗛 𝗟𝗢𝗚", callback_data="admin_crashes"),
                InlineKeyboardButton("🗑️ 𝗖𝗟𝗘𝗔𝗥", callback_data="admin_clear")
            ],
            [
                InlineKeyboardButton("◀️ 𝗕𝗔𝗖𝗞", callback_data="main_menu")
            ]
        ]
        return InlineKeyboardMarkup(keyboard)
    
    @staticmethod
    def shop_menu():
        """🏪 Shop Menu"""
        keyboard = [
            [
                InlineKeyboardButton("⭐ 𝗣𝗥𝗘𝗠𝗜𝗨𝗠 - 50💰", callback_data="shop_premium"),
                InlineKeyboardButton("💀 𝗖𝗥𝗔𝗦𝗛 𝗣𝗔𝗖𝗞 - 25💰", callback_data="shop_crashpack")
            ],
            [
                InlineKeyboardButton("🎫 𝗕𝗢𝗡𝗨𝗦 𝗣𝗔𝗖𝗞 - 10💰", callback_data="shop_bonus"),
                InlineKeyboardButton("🛡️ 𝗣𝗥𝗢𝗧𝗘𝗖𝗧 - 30💰", callback_data="shop_protect")
            ],
            [
                InlineKeyboardButton("◀️ 𝗕𝗔𝗖𝗞", callback_data="main_menu")
            ]
        ]
        return InlineKeyboardMarkup(keyboard)
    
    @staticmethod
    def settings_menu():
        """⚙️ Settings Menu"""
        keyboard = [
            [
                InlineKeyboardButton("🔔 𝗡𝗢𝗧𝗜𝗙𝗜𝗖𝗔𝗧𝗜𝗢𝗡𝗦", callback_data="settings_notify"),
                InlineKeyboardButton("🌙 𝗗𝗔𝗥𝗞 𝗠𝗢𝗗𝗘", callback_data="settings_dark")
            ],
            [
                InlineKeyboardButton("🌐 𝗟𝗔𝗡𝗚𝗨𝗔𝗚𝗘", callback_data="settings_lang"),
                InlineKeyboardButton("🔒 𝗣𝗥𝗜𝗩𝗔𝗖𝗬", callback_data="settings_privacy")
            ],
            [
                InlineKeyboardButton("◀️ 𝗕𝗔𝗖𝗞", callback_data="main_menu")
            ]
        ]
        return InlineKeyboardMarkup(keyboard)
    
    @staticmethod
    def confirm_menu(action, data):
        """✅ Confirm/Cancel Menu"""
        keyboard = [
            [
                InlineKeyboardButton("✅ 𝗖𝗢𝗡𝗙𝗜𝗥𝗠", callback_data=f"confirm_{action}_{data}"),
                InlineKeyboardButton("❌ 𝗖𝗔𝗡𝗖𝗘𝗟", callback_data="main_menu")
            ]
        ]
        return InlineKeyboardMarkup(keyboard)