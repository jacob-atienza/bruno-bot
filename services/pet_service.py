import os
import sqlite3
from datetime import date, datetime, timedelta
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError
from dotenv import load_dotenv

# Created 3/21/2026
# By Jacob Atienza
# Logic for interacting with the pet streaks table in the database

load_dotenv()

DB_PATH = os.getenv("DB_PATH")
PET_TIMEZONE = os.getenv("PET_TIMEZONE", os.getenv("TZ", "America/Toronto"))

if not DB_PATH:
    raise RuntimeError("DB_PATH is missing from .env")

try:
    PET_TIMEZONE_INFO = ZoneInfo(PET_TIMEZONE)
except ZoneInfoNotFoundError as exc:
    raise RuntimeError(
        f"Invalid PET_TIMEZONE '{PET_TIMEZONE}'. Use an IANA timezone like 'America/Toronto'."
    ) from exc

# Returns a connection to the sqlite DB
def get_connection():
    return sqlite3.connect(DB_PATH)


def get_today_for_pet_streak() -> date:
    return datetime.now(PET_TIMEZONE_INFO).date()

# Initialize the DB and create the pet streaks table if it doesn't already exist
def init_bruno_db():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS pet_streaks (
            user_id TEXT PRIMARY KEY,
            streak INTEGER NOT NULL,
            last_pet_date TEXT NOT NULL
            )
    """)

    conn.commit()
    conn.close()

# The  logic for creating + continuing a daily pet streak
def pet_user(user_id: int):
    today = get_today_for_pet_streak()
    yesterday = today - timedelta(days=1)
    user_id = str(user_id)

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT streak, last_pet_date FROM pet_streaks WHERE user_id = ?",
        (user_id,)
    )
    row = cursor.fetchone()

    if row is None:
        streak = 1
        cursor.execute(
            "INSERT INTO pet_streaks (user_id, streak, last_pet_date) VALUES (?, ?, ?)",
            (user_id, streak, today.isoformat())
        )
        conn.commit()
        conn.close()
        return {
            "counted_today": True,
            "streak": streak,
            "message": "You pet Bruno! Your streak has begun."
        }
    
    streak, last_pet_date = row
    last_pet_date = date.fromisoformat(last_pet_date)

    if last_pet_date == today:
        conn.close()
        return {
            "counted_today": False,
            "streak": streak,
            "message": "You already added to your streak today, but Bruno appreciates the love"
        }
    
    if last_pet_date == yesterday:
        streak += 1
    else: 
        streak = 1

    cursor.execute(
        "UPDATE pet_streaks SET streak = ?, last_pet_date = ? WHERE user_id = ?",
        (streak, today.isoformat(), user_id)
    )
    conn.commit()
    conn.close()

    return {
        "counted_today": True,
        "streak": streak,
        "message": "You pet Bruno"
    }

# fetches the streak of a given user
def get_user_streak(user_id: int):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT streak, last_pet_date FROM pet_streaks WHERE user_id = ?",
        (str(user_id),)
    )
    row = cursor.fetchone()
    conn.close()

    if row is None:
        return {"streak": 0, "last_pet_date": None}

    return {
        "streak": row[0],
        "last_pet_date": row[1]
    }

# fetches a leaderboard of users with the highest streaks
def get_pet_leaderboard(limit: int = 10):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT user_id, streak FROM pet_streaks ORDER BY streak DESC, last_pet_date DESC LIMIT ?",
        (limit,)
    )
    rows = cursor.fetchall()
    conn.close()

    return rows
