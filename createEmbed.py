import requests
import nextcord
from math import ceil


# want: profile, ranks instead of player, rank
def createPlayerEmbed(profile, ranks, Season, interaction, result):
    displayName = profile['displayName']
    score = ranks['score']

    avatar = profile['equippedAvatarURL']
    wins = profile['rankedStats']['wins']
    draws = profile['rankedStats']['draws']
    losses = profile['rankedStats']['losses']
    # winStreak = profile['rankedStats']['win_streak']
    highestWinStreak = profile['rankedStats']['highest_win_streak']
    color = int("A020F0", 16) if profile["is_vip"] else None
    minUses = float('inf')
    for item in profile["_towers"]:
        if item["used"] < minUses and item["type"] not in ["Quincy", "Quincy_Cyber", "Gwendolin", "Gwendolin_Science", "Obyn", "Obyn_Ocean", "StrikerJones", "StrikerJones_Biker", "Churchill", "Churchill_Sentai", "Benjamin", "Benjamin_DJ", "Ezili", "Ezili_SmudgeCat", "PatFusty", "PatFusty_Snowman", "Adora", "Adora_JoanOfArc", "BananaFarmer", "RoboBloon"]:
            minUses = item["used"]
            minTower = item["type"]

    totalPlayers = ranks['totalScores']

    em = nextcord.Embed(title=displayName, url=profile['matches'][:-7]+"?pretty=true",
                        description=f"Showing stats for #{ranks['rank']}/{totalPlayers}: {displayName}", color=color)
    em.set_thumbnail(avatar)
    # em.set_author(name=interaction.user.name)

    em.add_field(name='Score', value=score, inline=False)
    em.add_field(name='Wins', value=wins, inline=True)
    em.add_field(name='Draws', value=draws, inline=True)
    em.add_field(name="Losses", value=losses, inline=True)
    em.add_field(name="Highest Win Streak",
                 value=highestWinStreak, inline=False)
    em.add_field(name="Least Used Tower", value=f"{minTower}: {minUses}")
    em.set_footer(text="Data is from the official Ninja Kiwi API, updated about every 5 minutes.",
                  icon_url=interaction.guild.icon.url if interaction.guild.icon else interaction.user.avatar.url)

    result[0] = em


def createLeaderboardEmbed(page, season, interaction, result):
    apiPage = (page-1)//5+1
    endpoint = f"https://data.ninjakiwi.com/battles2/homs/season_{season-1}/leaderboard?page={apiPage}"
    allPlayers = requests.get(endpoint).json()['body']

    start = (page-1) % 5*10
    lenPage = min([10, len(allPlayers)-start])
    # damn, this solution is garage
    interestingPlayers = allPlayers[start:start+lenPage]

    em = nextcord.Embed(title=f"Showing players {start+1+50*(apiPage-1)}-{start+lenPage+50*(apiPage-1)}",
                        url=endpoint+"&pretty=true", color=int("FFFF00", 16))
    # em.set_author(name=interaction.user.name)

    ranks = ""
    for i in range(1, 1+lenPage):
        ranks += str((page-1)*10+i)+"\n"
    ranks = ranks[:-1]  # removes last newline
    em.add_field(name="Rank", value=ranks, inline=True)

    displayNames = ""
    for i in range(lenPage):
        try:
            displayNames += interestingPlayers[i]['displayName']+"\n"
        except:
            print("interesting players", interestingPlayers)
            print("page", page)
            print("endpoint", endpoint)
    displayNames = displayNames[:-1]
    em.add_field(name="Username", value=displayNames, inline=True)

    scores = ""
    for i in range(lenPage):
        scores += str(interestingPlayers[i]['score'])+"\n"
    scores = scores[:-1]
    em.add_field(name="Score", value=scores, inline=True)

    result[0] = em


# def createTimeoutEmbed(usernames):
#     with open("buttonLB.txt") as f:
#         data = f.readlines()

#     def epic_sort(item):
#         return int(item.split(" ")[1])
#     data.sort(key=epic_sort, reverse=True)

#     em = nextcord.Embed(title="Timeout Leaderboard", url="https://discord.com/channels/921447683154145331/921456054435455133/1091455632915308697", color=int("F1C40F", 16))  # big red button link, shiny color

#     users = ""
#     timeouts = ""
#     for i in range(min(10, len(data))):
#         userID = int(data[i].split(" ")[0])
#         # adds the username to the users list
#         users += await client.fetch_user(userID).username + "\n"
#         # adds timeouts to timeouts list
#         timeouts += data[i].split(" ")[1] + "\n"

#     em.add_field(name="Username", value=users, inline=True)
#     em.add_field(name="# Timeouts", value=timeouts, inline=True)

#     return em
