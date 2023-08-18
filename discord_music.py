import asyncio
import io

import discord
from discord.ext import commands, tasks
from discord.utils import get
from discord.voice_client import VoiceClient
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


# @tasks.loop(seconds=5)
"""async def check_voice_channel():
    print('loop')
    for voice_client in bot.voice_clients:
        if len(voice_client.channel.members) == 1:
            await voice_client.disconnect()
            channel_name = voice_client.channel.name
            await bot.get_channel(voice_client.channel.id).send(f"Left {channel_name} due to inactivity.")

async def before_check_voice_channel():
    await bot.wait_until_ready()"""

sources = ["The Last Chance (Rio & Aoi Version).mp3"]


async def custom_probe(source, executable):
    codec = "opus"
    bitrate = 128

    return codec, bitrate


async def play(ctx):
    if ctx.author.voice:
        channel = ctx.author.voice.channel
        voice_client: VoiceClient = get(bot.voice_clients, guild=ctx.guild)

        if voice_client and voice_client.is_connected():
            if voice_client.channel == channel:
                await ctx.send("I am already in your voice channel.")
            else:
                await voice_client.move_to(channel)
                await ctx.send(f"Moved to {channel.name}")
        else:
            voice_client = await channel.connect()
            await ctx.send(f"Entering {channel.name}")

        to_play = random.choice(sources)

        # OpusAudio.from_probe
        """source = await discord.FFmpegOpusAudio.from_probe(
            to_play,
            executable=r"D:/coding_workspace/Discord/ffmpeg-6.0-essentials_build/bin/ffmpeg.exe",
            method="fallback",
        )
        voice_client.play(source)"""

        # PC Audio
        voice_client.play(
            (
                discord.FFmpegPCMAudio(
                    executable=r"D:/coding_workspace/Discord/ffmpeg-6.0-essentials_build/bin/ffmpeg.exe",
                    source=to_play,
                )
            ),
            after=lambda e: print("Done", e),
        )
        await ctx.send(f"Playing: {to_play}")
    else:
        await ctx.send("You must be in a voice channel!")
