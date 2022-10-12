import os
from nextcord import Interaction, SlashOption, ChannelType
from nextcord.abc import GuildChannel
from nextcord.ext import commands, application_checks
import nextcord
import time

from convert import convert
from createbracket import createbracket

client = commands.Bot(command_prefix = "m!", intents = nextcord.Intents.all())
testingServersIDs = [627917374347149334, 921447683154145331] #JazzyJonah, B2T
@client.event
async def on_ready():
	print("hello")
	await client.sync_all_application_commands()
	await client.change_presence(activity = nextcord.Game(name="Battles 2"))

@client.slash_command(name="info", description="View info about the bot", guild_ids=testingServersIDs)
async def help(interaction: Interaction):
	await interaction.response.send_message("""
		**List of Commands** \n
		`/info` - What you're seeing right now!
		`/trailer` - Shows the official trailer for the B2T server
		`/create_tournament` - Creates a tournament (mod only) (WIP)\n
		||Created by JazzyJonah (<@627917067332485120>) - Source code: https://github.com/JazzyJonah/tourney-bot||""")

@client.slash_command(name="trailer", description="The official trailer for B2T", guild_ids=testingServersIDs)
async def trailer(interaction: Interaction):
	await interaction.response.send_message("https://www.youtube.com/watch?v=hn5jQF6KRok")

@client.slash_command(name="create_tourney", description="Create a tournament! (Mod only)", guild_ids=testingServersIDs)
@application_checks.check_any(application_checks.is_owner(), application_checks.has_any_role(929782523146432562, 845011146552508437)) #Tournament Admin, new role
async def create_tourney(
	interaction:Interaction,
	date_time: str=SlashOption(
		name="date_time",
		description="Date/time (format: MM/DD/YY HH:MM Timezone, eg. 04/16/22 15:45 EST)",
		required=True
	)
):
	try:
		vrej = convert(date_time.rsplit(" ",1)[0], date_time.split()[-1])
		await interaction.response.send_message("Tournament starts at <t:" + vrej + "> or <t:" + vrej + ":R>")
	except Exception as e:
		await interaction.response.send_message("You messed up somewhere. Try again. (Error message: " + str(e)) + ")"

	os.remove("bracket.png")
@create_tourney.error
async def on_create_tourney_error(interaction: Interaction, error):
  await interaction.response.send_message("You don't have tournament admin.")


@client.slash_command(name="send_bracket", description="Sends a bracket of some cool players", guild_ids=testingServersIDs)
async def send_bracket(interaction:Interaction):
	createbracket("Ninjayas", "https://cdn.discordapp.com/avatars/617541280154517641/b38841e95f8cdc0fb8b0374311b7e3e0.png", "JazzyJonah", "https://cdn.discordapp.com/avatars/627917067332485120/195cb543f9006e9024401fe3d6a871cc.png", "B2T", "https://cdn.discordapp.com/avatars/900469656844914729/8e7fe6eebdaf22ff691e477f79fd6ad5.png", "SSAMBO", "https://cdn.discordapp.com/avatars/920358051893104671/b512e4cc93b81134716892b9e08afe5f.png")
	await interaction.response.send_message(file=nextcord.File("bracket.png"))
	os.remove("bracket.png")



client.run(os.getenv("token"))
