import discord

from discord import Embed, Interaction, Color
from discord.ext import commands
from discord.ui import View, Button

from discordBot_settings import *


class RoleAssignmentView(discord.ui.View):
    def __init__(self, roles):
        super().__init__(timeout=60)
        options = []
        for role, emoji in roles:
            options.append(discord.SelectOption(label=role, emoji=emoji, value=role))

        self.select = discord.ui.Select(placeholder="Select a role", options=options)
        self.add_item(self.select)
        
    async def interaction_check(self, interaction: discord.Interaction) -> bool:
        return interaction.user == self.message.author

    async def on_timeout(self):
        await self.message.channel.send("Timeout")
        await self.disable_all_items()
        
    async def disable_all_items(self):
        for item in self.children:
            item.disabled = True
        await self.message.edit(view=self)
        
    async def on_select(self, interaction: discord.Interaction, select: discord.ui.Select):
        selected = select.values[0]
        role = discord.utils.get(interaction.guild.roles, name=selected)
        
        if role:
            await interaction.user.add_roles(role)
            await interaction.response.send_message(f"Assigned role: {selected}", ephemeral=True)
        else:
            await interaction.response.send_message("Role not found", ephemeral=True)
        
        await self.disable_all_items()
        self.stop()

async def create_role(ctx, *args):
    if len(args) % 2 != 0:
        await ctx.send("Wrong format. Example: !create_role [name of role] [emoji] [name of role] [emoji]...")
        return
    
    roles = list(zip(args[::2], args[1::2]))
    
    for role_name, emoji in roles:
        await ctx.guild.create_role(name=role_name)
        
    view = RoleAssignmentView(roles)
    message = await ctx.send("Choose a role:", view=view)
    view.message = message
    
    await view.wait()
    
    if view.timeout:
        await view.disable_all_items()
        print("Timeout")
    else:
        print("Role assigned!")

async def create_role_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send(
            "Wrong format. Example:\n`!create_role [name of role] [emoji] [name of role] [emoji]...`"
        )
    else:
        await ctx.send(str(error))