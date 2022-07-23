from xml.dom.expatbuilder import ParseEscape
import discord
from discord.ext import commands
from config import DISCORD_TOKEN
import os
import asyncio

bot = commands.Bot(command_prefix='=', intents=discord.Intents.all(), help_command=None)

@bot.command()
async def load(ctx, extension):
        await bot.load_extension(f"cogs.{extension}")
        await ctx.send("Load")



@bot.command()
async def sync(ctx):
        await bot.tree.sync()
        await ctx.send('Sync tree')

@bot.command()
async def unload(ctx, extension):
        await bot.unload_extension(f"cogs.{extension}")
        await ctx.send("Unload")


@bot.command()
async def reload(ctx, extension):
        await bot.unload_extension(f"cogs.{extension}")
        await bot.load_extension(f"cogs.{extension}")
        await ctx.send("Reload")

async def main():
    async with bot:
        await load_extensions()
        await bot.start(DISCORD_TOKEN)


async def load_extensions():
    for filename in os.listdir("./cogs"):
        if filename.endswith(".py"):
            print(f'Load: {filename[:-3]}')
            await bot.load_extension(f"cogs.{filename[:-3]}")
    print('All cogs loaded.')

asyncio.run(main())