import threading
import os
from nextcord import Interaction, SlashOption, ChannelType
from nextcord.abc import GuildChannel
from nextcord.ext import commands, application_checks
import nextcord
import datetime
from random import random, choice, shuffle
from math import floor
import requests
import json

from getPlayerMap import getPlayerMap
from convert import convert
from betterBracket import createbracket, Player
try:
	from tokenSucks import tokenSucks, imgurSucks
except:
	pass

client = commands.Bot(command_prefix = "m!", intents = nextcord.Intents.all())
testingServersIDs = [627917374347149334, 921447683154145331, 922420426175557632] #JazzyJonah, B2T, antarctica
@client.event
async def on_ready():
	print("hello")
	await client.sync_all_application_commands()
	await client.change_presence(activity = nextcord.Game(name="Bloons TD Battles 2"))

@client.event
async def on_message(message):
	pass
	# if "<@188217700697243648>" in message.content:
	# 	if not message.author.bot:
	# 		try: 
	# 			await message.author.edit(timeout=nextcord.utils.utcnow()+datetime.timedelta(seconds=4233600))
	# 		except Exception as e:
	# 			await message.channel.send("I can't time you out! Error message: `"+str(e)+"`")
	# 		await client.get_channel(926936642181271592).send(f"{message.author.mention} pinging sam")
	# 		await client.get_channel(979453104233799740).send(f"https://discord.com/channels/921447683154145331/{message.channel.id}/{message.id}: {message.author.display_name} pinged sam")

@client.slash_command(name="info", description="View info about the bot", guild_ids=testingServersIDs)
async def info(interaction: Interaction):
	if random() < 0.01:
		await interaction.response.send_message("NO, NOW SHUT UP BOZO")
	else:
		await interaction.response.send_message("""
			**List of Commands** \n
			`/info` - What you're seeing right now!
			`/trailer` - Shows the official trailer for the B2T server
			`/create_tournament` - Creates a tournament (mod only) (WIP)
			`/bracket` - Sends a bracket of some cool players (WIP)\n
			||Created by JazzyJonah - Source code: https://github.com/JazzyJonah/tourney-bot||""")

@client.slash_command(name="trailer", description="The official trailer for B2T", guild_ids=testingServersIDs)
async def trailer(interaction: Interaction):
	if random() < 0.01:
		await interaction.response.send_message("NO, NOW SHUT UP BOZO")
	else:
		await interaction.response.send_message("https://www.youtube.com/watch?v=hn5jQF6KRok")
@client.slash_command(name="map", description="Generate a random HoM map for the tourney", guild_ids=testingServersIDs)
async def map(interaction:Interaction):
	await interaction.response.send_message(choice(["Basalt Columns", "Inflection", "Building Site", "Castle Ruins", "Koru", "Dino Graveyard", "Oasis", "Garden", "Glade", "Ports", "Sands of Time", "Star"]))



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
	if random() < 0.01:
		await interaction.response.send_message("NO, NOW SHUT UP BOZO")
	else:
		try:
			vrej = convert(date_time.rsplit(" ",1)[0], date_time.split()[-1])
			await interaction.response.send_message("Tournament starts at <t:" + vrej + "> or <t:" + vrej + ":R>")
		except Exception as e:
			await interaction.response.send_message("You messed up somewhere. Try again. (Error message: " + str(e)) + ")"

	# os.remove("bracket.png")
@create_tourney.error
async def on_create_tourney_error(interaction: Interaction, error):
  await interaction.response.send_message("You don't have tournament admin.")


# class Winner(nextcord.ui.View):
# 	def __init__(self, player0="", player1=""):
# 		super().__init__()
# 		self.player0=player0
# 		self.player1=player1
# 		self.value=None

# 	@nextcord.ui.button(label=self.player0, style=nextcord.ButtonStyle.grey)
# 	async def player0(self, button:nextcord.ui.button, interaction:Interaction):
# 		self.value=self.player0
# 		self.stop()

# 	@nextcord.ui.button(label=self.player1, style=nextcord.ButtonStyle.grey)
# 	async def player0(self, button:nextcord.ui.button, interaction:Interaction):
# 		self.value=self.player1
# 		self.stop()

@client.slash_command(name="bracket", description="Sends a bracket of some cool players", guild_ids=testingServersIDs)
async def bracket(
	interaction:Interaction,
	player1: nextcord.Member=SlashOption(
		name="player1",
		description="First player",
		required=True
	),
	player2: nextcord.Member=SlashOption(
		name="player2",
		description="Second player",
		required=True
	),
	player3: nextcord.Member=SlashOption(
		name="player3",
		description="Third player",
		required=False
	),
	player4: nextcord.Member=SlashOption(
		name="player4",
		description="Fourth player",
		required=False
	),
	player5: nextcord.Member=SlashOption(
		name="player5",
		description="Fifth player",
		required=False
	),
	player6: nextcord.Member=SlashOption(
		name="player6",
		description="Sixth player",
		required=False
	),
	player7: nextcord.Member=SlashOption(
		name="player7",
		description="Seventh player",
		required=False
	),
	player8: nextcord.Member=SlashOption(
		name="player8",
		description="Eigth player",
		required=False
	),
	player9: nextcord.Member=SlashOption(
		name="player9",
		description="Ninth player",
		required=False
	),
	player10: nextcord.Member=SlashOption(
		name="player10",
		description="Tenth player",
		required=False
	),
	player11: nextcord.Member=SlashOption(
		name="player11",
		description="Eleventh player",
		required=False
	),
	player12: nextcord.Member=SlashOption(
		name="player12",
		description="Twefth player",
		required=False
	),
	player13: nextcord.Member=SlashOption(
		name="player13",
		description="Thirteenth player",
		required=False
	),
	player14: nextcord.Member=SlashOption(
		name="player14",
		description="Fourteenth player",
		required=False
	),
	player15: nextcord.Member=SlashOption(
		name="player15",
		description="Fifteenth player",
		required=False
	),
	player16: nextcord.Member=SlashOption(
		name="player16",
		description="Sixteenth player",
		required=False
	),

):
	if random() < 0.01:
		await interaction.response.send_message("NO, NOW SHUT UP BOZO")
	else:
		await interaction.response.defer()
		players=[]
		if True: #for collapsing - appends a bunch of stuff to players
			players.append(Player(player1.name, player1.display_avatar, 0))
			players.append(Player(player2.name, player2.display_avatar, 0))
			if player3:
				players.append(Player(player3.name, player3.display_avatar, 0))
				if player4:
					players.append(Player(player4.name, player4.display_avatar, 0))
					if player5:
						players.append(Player(player5.name, player5.display_avatar, 0))
						if player6:
							players.append(Player(player6.name, player6.display_avatar, 0))
							if player7:
								players.append(Player(player7.name, player7.display_avatar, 0))
								if player8:
									players.append(Player(player8.name, player8.display_avatar, 0))
									if player9:
										players.append(Player(player9.name, player9.display_avatar, 0))
										if player10:
											players.append(Player(player10.name, player10.display_avatar, 0))
											if player11:
												players.append(Player(player11.name, player11.display_avatar, 0))
												if player12:
													players.append(Player(player12.name, player12.display_avatar, 0))
													if player13:
														players.append(Player(player13.name, player13.display_avatar, 0))
														if player14:
															players.append(Player(player14.name, player14.display_avatar, 0))
															if player15:
																players.append(Player(player15.name, player15.display_avatar, 0))
																if player16:
																	players.append(Player(player16.name, player16.display_avatar, 0))

		
		shuffle(players)
		result=[None, None] #this is just a length 2 list because threading is dumb - first item is url of imgbb thing, second item is matches for next round
		backgroundBracket = threading.Thread(target = createbracket, name = '', args = (players, result)) # this is so it doesn't block out nextcord
		backgroundBracket.start()
		while backgroundBracket.is_alive(): # waits until program is finished while not blocking anything
			pass
		await interaction.followup.send(result[0])#, view=Winner("Heli ice"))
		os.remove("bracket.png")

# @client.slash_command(name="leaderboard", description="Sends the t10 current players in Battles 2!", guild_ids=testingServersIDs)
# async def leaderboard(interaction:Interaction):
# 	import requests
# 	import json
# 	r=requests.get("https://fast-static-api.nkstatic.com/storage/static/appdocs/17/leaderboards/lb:hom_rank:season_8:public.json", headers={"user-agent":"battles2-1.7.2"}, data={"key":"value"})
# 	r.json()
# 	data = json.loads(json.loads(r.text)['data'])
# 	message=""
# 	for i in range(10):
# 		try:
# 			message+=f'#{i+1}: {getPlayerMap()[data["scores"]["equal"][i]["userID"]]}\n'
# 		except:
# 			message+=f'#{i+1}: unknown\n'
# 	await interaction.response.send_message("```"+message+"```")


if os.getenv("token")!= None:
	client.run(os.getenv("token"))
else:
	client.run(tokenSucks())