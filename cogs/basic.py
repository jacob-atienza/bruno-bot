import discord
from discord import app_commands
from discord.ext import commands

class Basic(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(name="ping", description="Check if the bot is alive")
    async def ping(self, interaction: discord.Interaction):
        await interaction.response.send_message(f"Pong! {round(self.bot.latency * 1000)} ms")

    @app_commands.command(name="hello", description="Say hello")
    async def hello(self, interaction: discord.Interaction):
        await interaction.response.send_message(f"Hey, {interaction.user.mention}!")

    @app_commands.command(name="say", description="Make the bot say something")
    @app_commands.describe(message="What you want the bot to say")
    async def say(self, interaction: discord.Interaction, message: str):
        await interaction.response.send_message(message)

    @app_commands.command(name="serverinfo", description="Show server information")
    async def serverinfo(self, interaction: discord.Interaction):
        guild = interaction.guild

        if guild is None:
            await interaction.response.send_message("This command can only be used in a server.")
            return

        embed = discord.Embed(title=guild.name)
        embed.add_field(name="Server ID", value=str(guild.id), inline=False)
        embed.add_field(name="Members", value=str(guild.member_count), inline=False)
        embed.add_field(name="Owner ID", value=str(guild.owner_id), inline=False)

        if guild.icon:
            embed.set_thumbnail(url=guild.icon.url)

        await interaction.response.send_message(embed=embed)

async def setup(bot: commands.Bot):
    await bot.add_cog(Basic(bot))