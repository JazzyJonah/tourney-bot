import os
from nextcord import Interaction, SlashOption, ChannelType
from nextcord.abc import GuildChannel
from nextcord.ext import commands, application_checks
import nextcord
import time

from convert import convert

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
		||Created by JazzyJonah (<@627917067332485120>); Source code: https://github.com/JazzyJonah/tourney-bot||""")

@client.slash_command(name="trailer", description="The official trailer for B2T", guild_ids=testingServersIDs)
async def trailer(interaction: Interaction):
	await interaction.response.send_message("https://www.youtube.com/watch?v=hn5jQF6KRok")

@client.slash_command(name="create_tourney", description="Create a tournament! (Mod only)", guild_ids=testingServersIDs)
@application_checks.check_any(application_checks.is_owner(), application_checks.has_any_role(929782523146432562, 845011146552508437)) #Tournament Admin, new role
async def create_tourney(
	interaction:Interaction,
	date_time: str=SlashOption(
		name="date_time",
		description="What date/time you want the tourney to start. (Format: MM/DD/YY HH:MM:SS Timezone, eg. 04/16/22 15:45:00 EST)",
		required=True
	)
):
	await interaction.response.send_message(convert(date_time.rsplit(" ",1)[0], date_time.split()[-1]))




client.run(os.getenv("token"))
