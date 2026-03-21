import os
import asyncio
import discord
from discord.ext import commands
from dotenv import load_dotenv
from services.pet_service import init_bruno_db

load_dotenv()

TOKEN = os.getenv("DISCORD_TOKEN")
GUILD_ID = os.getenv("DISCORD_GUILD_ID")

if not TOKEN:
    raise RuntimeError("DISCORD_TOKEN is missing from .env")

if not GUILD_ID:
    raise RuntimeError("DISCORD_GUILD_ID is missing from .env")

intents = discord.Intents.default()
bot = commands.Bot(command_prefix="!", intents=intents)

async def load_cogs():
    await bot.load_extension("cogs.basic")
    await bot.load_extension("cogs.homelab")
    await bot.load_extension("cogs.pet")

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user} (ID: {bot.user.id})")

    try:
        guild = discord.Object(id=int(GUILD_ID))

        bot.tree.copy_global_to(guild=guild)
        synced = await bot.tree.sync(guild=guild)

        print(f"Synced {len(synced)} command(s) to guild {GUILD_ID}")
        for command in synced:
            print(f"- /{command.name}")

    except Exception as e:
        print(f"Failed to sync commands: {e}")

async def main():
    init_bruno_db()
    async with bot:
        await load_cogs()
        await bot.start(TOKEN)

if __name__ == "__main__":
    asyncio.run(main())