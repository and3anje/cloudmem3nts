#!/usr/bin/env python3
import os
import shutil
import datetime

def log_message(message):
    timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    log_entry = f"[{timestamp}] {message}"
    
    with open("cloud.log", "a") as f:
        f.write(log_entry + "\n")
    
    print(log_entry)

def check_disk():
    total, used, free = shutil.disk_usage('/')
    
    total_gb = total / (1024**3)
    used_gb = used / (1024**3)
    free_gb = free / (1024**3)
    percent = (used_gb / total_gb) * 100
    
    if percent > 70:
        log_message(f"WARNING: Disk usage at {percent:.1f}% — {free_gb:.1f}GB free")
    else:
        log_message(f"OK: Disk usage at {percent:.1f}% — {free_gb:.1f}GB free")

def read_log():
    print("\n--- Log Contents ---")
    with open("cloud.log", "r") as f:
        print(f.read())

log_message("Script started")
check_disk()
log_message("Script complete")
read_log()

def safe_read_file(filepath):
    try:
        with open(filepath, "r") as f:
            content = f.read()
            log_message(f"OK: Read {filepath} successfully")
            return content
    except FileNotFoundError:
        log_message(f"WARNING: {filepath} not found")
        return None
    except PermissionError:
        log_message(f"WARNING: No permission to read {filepath}")
        return None
    finally:
        log_message("File read attempt complete")

# Test all three cases
safe_read_file("cloud.log")
safe_read_file("nonexistent.txt")
safe_read_file("/etc/shadow")