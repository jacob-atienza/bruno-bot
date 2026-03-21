# cogs/homelab.py
import discord
from discord import app_commands
from discord.ext import commands
from services.system_service import get_server_status
from services.docker_service import list_docker_containers

class Homelab(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="serverstatus", description="Show server CPU, RAM, and OS info.")
    async def serverstatus(self, interaction: discord.Interaction):
        status = get_server_status()
        await interaction.response.send_message(f"`{status}`", ephemeral=True)

    @app_commands.command(name="dockerlist", description="List running Docker containers.")
    async def dockerlist(self, interaction: discord.Interaction):
        containers = list_docker_containers()
        await interaction.response.send_message(
            f"```{containers}```", ephemeral=True)

async def setup(bot):
    await bot.add_cog(Homelab(bot))
