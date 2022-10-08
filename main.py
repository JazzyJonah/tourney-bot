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
	await interaction.response.send_message("""
		**List of Commands** \n
		`/info` - What you're seeing right now!
		`/trailer` - Shows the official trailer for the B2T server
		`/create_tournament` - Creates a tournament (mod only) (WIP)\n
		||Created by JazzyJonah (<@627917067332485120>); Source code: https://github.com/JazzyJonah/tourney-bot""")

@client.slash_command(name="trailer", description="The official trailer for B2T", guild_ids=testingServersIDs)
async def trailer(interaction: Interaction):
	await interaction.response.send_message("https://www.youtube.com/watch?v=hn5jQF6KRok")


client.run(os.getenv("token"))