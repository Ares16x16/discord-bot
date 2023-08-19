import random

import discord
from discord.ext import commands, tasks

import discord_poll
import discord_role
import discord_play
import discord_music
import discord_utils
from discordBot_settings import *


# On start
@bot.event
async def on_ready():
    """
    Say hi when start
    """
    print("Bot is ready")
    # channel = bot.get_channel()  # Test Server Main channel
    await channel.send("```Hi, I'm here```")


# Common Error
@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        await ctx.send(f"Unknown command. Use `{bot.command_prefix}help` for help.")


# Help
@bot.hybrid_command()
async def help(ctx):
    prefix = bot.command_prefix

    response = "**Bot Commands**\n\n"
    for command in bot.commands:
        if not command.hidden and command.name != "synccommands":
            response += f"**{command.name}**: {command.help if command.help else 'No description'}\n"
            response += f"Usage: `{prefix}{command.name} {command.signature}`\n\n"

    await ctx.send(response)


# Sync
@bot.command()
@commands.has_permissions(administrator=True)
async def synccommands(ctx):
    """
    Sync commands for "/" prefix
    """
    await bot.tree.sync()
    await ctx.send("Sync Completed")


@bot.hybrid_command()
async def ping(ctx):
    """
    Tradition ping test
    """
    await ctx.send("Pong")


### Poll ###
# Poll Reaction
@bot.command()
async def reaction_poll(ctx, title, question, *options):
    await discord_poll.poll_reaction(ctx, title, question, *options)


@reaction_poll.error
async def poll_reaction_error(ctx, error):
    await discord_poll.poll_reaction_error(ctx, error)


# Poll Button
@bot.command()
async def advance_poll(ctx, title, question, timeout, *options):
    await discord_poll.advance_poll(ctx, title, question, timeout, *options)


@advance_poll.error
async def advance_poll_error(ctx, error):
    await discord_poll.advance_poll_error(ctx, error)


### Role ###
# Roll creation
@bot.command()
async def create_role(ctx, channel, *roleset):
    await discord_role.create_role(ctx, channel, *roleset)


@create_role.error
async def create_role_error(ctx, error):
    await discord_role.create_role_error(ctx, error)


### Play ###
@bot.hybrid_command()
async def random_ping(ctx, verb="ping"):
    """
    You can ping a random guy with a verb
    """
    await discord_play.random_ping(ctx, verb)


@bot.hybrid_command()
async def dice(ctx, xdx="1d6"):
    """
    Dice!
    """
    await discord_play.dice(ctx, xdx)


### Voice Channel ###
# Need PyNaCl
# Basics
@bot.hybrid_command()
async def join(ctx):
    """
    Join the voice chat
    """
    await discord_music.join(ctx)


@bot.hybrid_command()
async def leave(ctx):
    """
    Leave the voice chat
    """
    await discord_music.leave(ctx)


@join.error
async def join_error(ctx, error):
    await discord_music.join_error(ctx, error)


@bot.hybrid_command()
async def play_random(ctx):
    await discord_music.play_random(ctx)


"""@bot.hybrid_command()
async def play(ctx, link):
    await discord_music.play(ctx, link)"""


@play_random.error
# @play.error
async def play_music_error(ctx, error):
    if isinstance(error):
        await ctx.send(str(error))


bot.run("")
