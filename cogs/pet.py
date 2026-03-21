import discord
from discord import app_commands
from discord.ext import commands
from io import BytesIO

from services.pet_service import pet_user, get_user_streak, get_pet_leaderboard
from services.immich_service import get_random_bruno_image_with_reason

class Pet(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot


    @app_commands.command(name="pet", description="Pet Bruno and keep your daily streak.")
    async def pet(self, interaction: discord.Interaction):
        result = pet_user(interaction.user.id)
        image_data, image_error = await get_random_bruno_image_with_reason()
        
        embed = discord.Embed(title="Pet Time")
        embed.description = result["message"]
        embed.add_field(
            name="Current Streak",
            value=f'{result["streak"]} day{"s" if result ["streak"] != 1 else ""}',
            inline=False
        )

        if result["counted_today"]:
            embed.add_field(name="Today", value="Counted towards streak", inline=False)
        else: 
            embed.add_field(name="Today", value="Already counted today", inline=False)

        if image_data:
            image_file = discord.File(
                BytesIO(image_data["bytes"]),
                filename=image_data["filename"]
            )
            embed.set_image(url=f'attachment://{image_data["filename"]}')
            await interaction.response.send_message(embed=embed, file=image_file)
            return

        footer_message = "Bruno image unavailable right now."
        if image_error:
            footer_message = f"{footer_message} ({image_error})"
        embed.set_footer(text=footer_message)
        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="petstreak", description="See your current pet streak.")
    async def petstreak(self, interaction: discord.Interaction):
        result = get_user_streak(interaction.user.id)

        embed = discord.Embed(title="Your Pet Streak")
        embed.add_field(
            name="Streak",
            value=f'{result["streak"]} day{"s" if result["streak"] != 1 else ""}',
            inline=False
        )

        if result["last_pet_date"]:
            embed.add_field(name="Last Pet", value=result["last_pet_date"], inline=False)

        await interaction.response.send_message(embed=embed, ephemeral=True)

    @app_commands.command(name="petleaderboard", description="Show the top pet streaks.")
    async def petleaderboard(self, interaction: discord.Interaction):
        rows = get_pet_leaderboard()

        if not rows:
            await interaction.response.send_message("Nobody has started a pet streak yet.")
            return

        embed = discord.Embed(title="🏆 Pet Leaderboard")

        lines = []
        for index, (user_id, streak) in enumerate(rows, start=1):
            lines.append(f"{index}. <@{user_id}> — {streak} day{'s' if streak != 1 else ''}")

        embed.description = "\n".join(lines)
        await interaction.response.send_message(embed=embed)

async def setup(bot: commands.Bot):
    await bot.add_cog(Pet(bot))
