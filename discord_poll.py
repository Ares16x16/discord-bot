import asyncio
import string

import discord
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
        embed.add_field(name=f"Option {chr(0x1f1e6 + i)}", value=option, inline=False)
    
    poll_message = await channel.send(embed=embed)
    
    for i in range(len(options)):
        await poll_message.add_reaction(chr(0x1f1e6 + i))
        
async def poll_reaction_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("Wrong format. Example: \n`!reaction_poll \"[TITLE_OF_POLL]\" \"[YOUR_QUESTION]\" \"[OPTIONS]\" \"[OPTIONS]\" \"[OPTIONS]\"`")
    else:
        await ctx.send("An error occurred while creating the poll. Please try again.")
        
# Poll using buttons        
"""class OptionButton(Button):
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
            
            await interaction.response.edit_message(embed=embed, view=self.view)"""
            
class PollView(discord.ui.View):
    def __init__(self, ctx, options, embed, advancePoll_user_id, timeout):
        super().__init__(timeout=int(timeout))
        self.ctx = ctx
        self.options = options
        self.embed = embed
        self.advancePoll_user_id = advancePoll_user_id
        
        for index, option in enumerate(options):
            #emoji = discord.utils.get(ctx.guild.emojis, name=f"option{index+1}")
            label = option
            button = discord.ui.Button(style=discord.ButtonStyle.secondary, label=label)
            self.add_item(button)
            
    async def on_timeout(self, interaction: discord.Interaction):
        for index, button in enumerate(self.children):
            button.disabled = True
               
    async def interaction_check(self, interaction: discord.Interaction) -> bool:
        await interaction.response.defer()
        
        custom_id = interaction.data["custom_id"] 
        
        # 1 vote per person
        if interaction.user.id in self.advancePoll_user_id:
            return
        else:
            self.advancePoll_user_id.append(interaction.user.id)
        
        #button_label = clicked_button.label
        sequence_number = 0
        for index, button in enumerate(self.children):
            if button.custom_id == custom_id:
                sequence_number = index
                break
        
        field_index = sequence_number
        field_value = self.embed.fields[field_index].value
        votes_start = field_value.rfind('-') + 1
        votes_end = field_value.rfind('votes')
        vote_number = int(field_value[votes_start:votes_end].strip())
        vote_number += 1

        self.embed.set_field_at(field_index, name=self.embed.fields[field_index].name, value=f"{vote_number} votes", inline=False)

        await interaction.message.edit(embed=self.embed, view=self)


async def advance_poll(ctx, title, question, timeout=600, *options):
    if len(options) < 2:
        await ctx.send("Please provide at least two options for the poll.")
        return

    if len(options) > 5:
        await ctx.send("You can only provide up to 5 options for the poll.")
        return
    
    emoji = [":one:",":two:",":three:",":four:",":five:"]
    embed = Embed(title=title, description=question, color=Color.blue())
    for index, option in enumerate(options):
        embed.add_field(name=f"{emoji[index]} {option}", value="0 votes", inline=False)
    advancePoll_user_id = []
    view = PollView(ctx, options, embed, advancePoll_user_id, timeout)
    
    message = await ctx.send(embed=embed, view=view)

async def advance_poll_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send(
            "Wrong format. Example: \n`!advance_poll \"[TITLE_OF_POLL]\" \"[YOUR_QUESTION]\" \"[TIMEOUT]\" \"[OPTIONS]\" \"[OPTIONS]\" \"[OPTIONS]\"`"
        )
    else:
        await ctx.send(str(error))