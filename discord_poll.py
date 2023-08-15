import asyncio
import discord
import string

from discord import Embed, Interaction, Color
from discord.ext import commands
from discord.ui import View, Button

from discordBot_settings import *


# Poll using embed and reaction
async def poll_reaction(ctx, title, question, *options):
    if not options:
        await ctx.send("ERROR: At least two options for the poll.")
        return
    
    channel_mention = ctx.message.channel_mentions
    channel = channel_mention[0] if channel_mention else ctx.channel
    
    embed = discord.Embed(title=title, description=question, color=discord.Color.blue())
    
    for i, option in enumerate(options):
        embed.add_field(name=f"Option {i+1}", value=option, inline=False)
    
    poll_message = await channel.send(embed=embed)
    
    for i in range(len(options)):
        await poll_message.add_reaction(chr(0x1f1e6 + i))
        
async def poll_reaction_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("Wrong format. Example: \n`!reactionPoll \"[TITLE_OF_POLL]\" \"[YOUR_QUESTION]\" \"[OPTIONS]\" \"[OPTIONS]\" \"[OPTIONS]\"`")
    else:
        await ctx.send("An error occurred while creating the poll. Please try again.")
        
# Poll using buttons        
class OptionButton(Button):
    def __init__(self, label, **kwargs):
        super().__init__(label=label, **kwargs)
        self.votes = 0

    async def callback(self, interaction: Interaction):
        if self.view.owner_id != interaction.user.id:
            self.votes += 1
            self.style = discord.ButtonStyle.success
            self.disabled = True
            
            embed = self.view.get_embed()
            for item in self.view.children:
                if isinstance(item, OptionButton):
                    option_label = f"{item.label}: {item.votes} votes"
                    embed.description = embed.description.replace(item.label, option_label)
            
            await interaction.response.edit_message(embed=embed, view=self.view)

class PollView(View):
    def __init__(self, ctx, options, timeout=60.0):
        super().__init__(timeout=timeout)
        self.owner_id = ctx.author.id
        for option in options:
            self.add_item(OptionButton(option))

    async def interaction_check(self, interaction: Interaction):
        return True  # Allow everyone to vote

    async def on_timeout(self):
        for item in self.children:
            if isinstance(item, OptionButton):
                item.disabled = True
        await self.message.edit(view=self)

async def advance_poll(ctx, title, question, *options):
    if len(options) < 2:
        await ctx.send("Please provide at least two options for the poll.")
        return

    if len(options) > 10:
        await ctx.send("You can only provide up to 10 options for the poll.")
        return
    
    embed = Embed(title=title, description=question, color=Color.blue())
    view = PollView(ctx, options)
    
    message = await ctx.send(embed=embed, view=view)

async def advance_poll_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send(
            "Wrong format. Example: \n`!advancePoll \"[TITLE_OF_POLL]\" \"[YOUR_QUESTION]\" \"[OPTIONS]\" \"[OPTIONS]\" \"[OPTIONS]\"`"
        )
    else:
        await ctx.send(str(error))