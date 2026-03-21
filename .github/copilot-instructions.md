# Project: Bruno Bot

## Context

This is a self-hosted Discord bot using discord.py.

The bot:

- runs locally on a home server
- uses slash commands (app_commands)
- is structured using cogs
- loads commands via bot.tree

## Structure

- bot.py = entry point
- cogs/ = command modules
- .env = contains DISCORD_TOKEN and DISCORD_GUILD_ID

## Rules for code generation

- Always use discord.py 2.x patterns
- Use app_commands for slash commands (not prefix commands unless asked)
- Place commands inside cogs
- Do not rewrite the entire project unless explicitly asked
- Prefer small, incremental changes

## Workflow rules

When implementing something:

1. Explain what you will do briefly
2. Show only necessary code changes
3. Do not invent unnecessary files
4. Keep things simple and readable

## Safety

- Never include tokens or secrets in code
- Do not modify .env
