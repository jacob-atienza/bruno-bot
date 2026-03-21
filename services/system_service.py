# services/system_service.py
"""
Provides system status utilities for the bot.
"""
import platform
import psutil

def get_server_status():
    """Returns a summary of system status."""
    try:
        cpu = psutil.cpu_percent(interval=0.5)
        mem = psutil.virtual_memory()
        return f"CPU: {cpu}% | RAM: {mem.percent}% ({mem.used // (1024**2)}MB/{mem.total // (1024**2)}MB) | OS: {platform.system()} {platform.release()}"
    except Exception as e:
        return f"Error retrieving status: {e}"