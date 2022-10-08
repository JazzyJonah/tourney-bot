import os
from nextcord import Interaction, SlashOption, ChannelType
from nextcord.abc import GuildChannel
from nextcord.ext import commands, application_checks
import nextcord

client = commands.Bot(command_prefix = "m!", intents = nextcord.Intents.all())

testingServersIDs = [627917374347149334, 921447683154145331] #JazzyJonah, B2T

@client.event
async def on_ready():
	print("hello")
	await client.sync_all_application_commands()

@client.slash_command(name="info", description="View info about the bot", guild_ids=testingServersIDs)
async def help(interaction: Interaction):
	await interaction.response.send_message("The test command works!")

client.run(os.getenv("token"))