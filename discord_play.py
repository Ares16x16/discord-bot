import random

import discord

from discordBot_settings import *

async def random_ping(ctx, verb="ping"):
    members = ctx.guild.members
    members = [member for member in members if not member.bot and member != ctx.author]
    random_member = random.choice(members)

    await ctx.send(f"{ctx.author.mention} {verb} {random_member.mention}")  
    
async def dice(ctx, xdx):
    number_of_dice, number_of_sides = map(int, xdx.split('d'))
    rolls = [random.randint(1, number_of_sides) for _ in range(number_of_dice)]

    total = sum(rolls)

    response = f"Rolling {xdx}:\n"
    response += "\n".join([f"Result {i + 1}: {roll}" for i, roll in enumerate(rolls)])
    response += f"\nTotal: {total}"

    await ctx.send("```"+response+"```")