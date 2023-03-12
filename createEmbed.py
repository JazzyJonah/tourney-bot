import requests
import nextcord
from math import ceil
def createPlayerEmbed(profile, ranks, Season, interaction, result): # want: profile, ranks instead of player, rank
	displayName = profile['displayName']
	score = ranks['score']

	avatar = profile['equippedAvatarURL']
	wins = profile['rankedStats']['wins']
	draws = profile['rankedStats']['draws']
	losses = profile['rankedStats']['losses']
	#winStreak = profile['rankedStats']['win_streak']
	highestWinStreak = profile['rankedStats']['highest_win_streak']
	color = int("A020F0", 16) if profile["is_vip"] else None
	minUses = float('inf')
	for item in profile["_towers"]:
		if item["used"] < minUses and item["type"] not in ["Quincy", "Quincy_Cyber", "Gwendolin", "Gwendolin_Science", "Obyn", "Obyn_Ocean", "StrikerJones", "StrikerJones_Biker", "Churchill", "Churchill_Sentai", "Benjamin", "Benjamin_DJ", "Ezili", "Ezili_SmudgeCat", "PatFusty", "PatFusty_Snowman", "Adora", "Adora_JoanOfArc", "BananaFarmer", "RoboBloon"]:
			minUses = item["used"]
			minTower = item["type"]

	totalPlayers = ranks['totalScores']

	em = nextcord.Embed(title = displayName, url = profile['matches']+"?pretty=true", description = f"Showing stats for #{ranks['rank']}/{totalPlayers}: {displayName}", color = color)
	em.set_thumbnail(avatar)
	# em.set_author(name=interaction.user.name)

	em.add_field(name = 'Score', value = score, inline = False)
	em.add_field(name = 'Wins', value = wins, inline = True)
	em.add_field(name = 'Draws', value = draws, inline = True)
	em.add_field(name = "Losses", value = losses, inline = True)
	em.add_field(name = "Highest Win Streak", value = highestWinStreak, inline = False)
	em.add_field(name = "Least Used Tower", value = f"{minTower}: {minUses}")
	em.set_footer(text = "Data is from the official Ninja Kiwi API, updated about every 5 minutes.", icon_url = interaction.guild.icon.url if interaction.guild.icon else interaction.user.avatar.url)

	result[0] = em


def createLeaderboardEmbed(page, season, interaction, result):
	apiPage = (page-1)//5+1
	endpoint = f"https://data.ninjakiwi.com/battles2/homs/season_{season-1}/leaderboard?page={apiPage}"
	allPlayers = requests.get(endpoint).json()['body']

	start = (page-1)%5*10
	lenPage=min([10, len(allPlayers)-start])
	interestingPlayers = allPlayers[start:start+lenPage] #damn, this solution is garage

	em = nextcord.Embed(title = f"Showing players {start+1+50*(apiPage-1)}-{start+lenPage+50*(apiPage-1)}", url = endpoint+"&pretty=true", color = int("FFFF00", 16))
	# em.set_author(name=interaction.user.name)

	ranks = ""
	for i in range(1, 1+lenPage):
		ranks+=str((page-1)*10+i)+"\n"
	ranks = ranks[:-1] # removes last newline
	em.add_field(name = "Rank", value = ranks, inline = True)

	displayNames = ""
	for i in range(lenPage):
		try:
			displayNames+=interestingPlayers[i]['displayName']+"\n"
		except:
			print("interesting players",interestingPlayers)
			print("page", page)
			print("endpoint", endpoint)
	displayNames = displayNames[:-1]
	em.add_field(name = "Username", value = displayNames, inline = True)

	scores = ""
	for i in range(lenPage):
		scores+=str(interestingPlayers[i]['score'])+"\n"
	scores = scores[:-1]
	em.add_field(name = "Score", value = scores, inline = True)

	result[0] = em
