#!/usr/bin/env python3
# Utility Functions
# Author: HeaNg[Black-Cyber]

import re
import time
from datetime import datetime

def format_number(num):
    """Format number with commas"""
    return f"{num:,}"

def validate_phone(phone):
    """Validate phone number"""
    # Remove any non-digit characters
    phone = re.sub(r'\D', '', phone)
    # Check if phone has at least 10 digits
    return len(phone) >= 10

def format_time(timestamp):
    """Format timestamp to readable time"""
    if isinstance(timestamp, str):
        timestamp = datetime.fromisoformat(timestamp)
    return timestamp.strftime("%Y-%m-%d %H:%M:%S")

def get_medal(rank):
    """Get medal emoji for rank"""
    if rank == 1:
        return "🥇"
    elif rank == 2:
        return "🥈"
    elif rank == 3:
        return "🥉"
    else:
        return f"{rank}."

def truncate_text(text, max_length=4000):
    """Truncate text to max length"""
    if len(text) <= max_length:
        return text
    return text[:max_length-3] + "..."

def generate_id():
    """Generate unique ID"""
    return f"{int(time.time())}_{random.randint(1000, 9999)}"

def parse_arguments(args):
    """Parse command arguments"""
    if not args:
        return None
    return ' '.join(args)

def is_admin(user_id, admin_ids):
    """Check if user is admin"""
    return user_id in admin_ids