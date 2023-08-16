import asyncio
import io

import discord
from discord.ext import commands, tasks
import youtube_dl
import random


from discordBot_settings import *

timeout_duration = 300  # seconds

"""@bot.event
async def on_ready():
    # Start the timeout check loop
    check_voice_channel.start()"""

### Basics ###
async def join(ctx):
    if ctx.author.voice:
        channel = ctx.author.voice.channel
        voice_client = await channel.connect()
        await ctx.send(f"Entering {channel.name}")
    else:
        await ctx.send("You must be in a voice channel!")

async def leave(ctx):
    if ctx.voice_client:
        await ctx.voice_client.disconnect()
        await ctx.send("Leaving VC")
    else:
        await ctx.send("I am not connected to a voice channel.")
        
async def join_error(ctx, error):
    if isinstance(error):
        await ctx.send(str(error))
        
#@tasks.loop(seconds=5)
"""async def check_voice_channel():
    print('loop')
    for voice_client in bot.voice_clients:
        if len(voice_client.channel.members) == 1:
            await voice_client.disconnect()
            channel_name = voice_client.channel.name
            await bot.get_channel(voice_client.channel.id).send(f"Left {channel_name} due to inactivity.")

async def before_check_voice_channel():
    await bot.wait_until_ready()"""
