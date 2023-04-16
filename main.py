import threading
import os
from nextcord import Interaction, SlashOption, ChannelType
from nextcord.abc import GuildChannel, Snowflake
from nextcord.ext import commands, application_checks
import nextcord
import datetime
from random import random, choice, shuffle
from math import floor
import requests
import json
import sys
import time
import cooldowns
from datetime import datetime, timedelta

from getPlayerMap import getPlayerMap
from convert import convert
from createEmbed import createPlayerEmbed, createLeaderboardEmbed#  , createTimeoutEmbed
from betterBracket import createbracket, Player
from updateLBTxt import updateLBTxt
from TimeoutView import TimeoutView
try:
    from tokenSucks import tokenSucks, imgurSucks
except:
    pass

client = commands.Bot(command_prefix="m!", intents=nextcord.Intents.all(), allowed_mentions=nextcord.AllowedMentions.none())
testingServersIDs = [627917374347149334, 921447683154145331, 922420426175557632]  # JazzyJonah, B2T, antarctica


@client.event
async def on_ready():
    print("hello")
    await client.sync_all_application_commands()
    await client.change_presence(activity=nextcord.Game(name="Bloons TD Battles 2"))

    #perma button
    if(len(client.persistent_views)==0):
        client.add_view(TimeoutView(client))
    # await client.get_channel(921456054435455133).send("Click here to get timed out!", view=TimeoutView(client))
    # await client.get_channel(1029501175009116200).send("Some new *secrets* have been added! Have fun trying to find them, and definitely don't just look at the source code. --- 12 March 2023")

    #print(client.guilds[4].get_role(1029498546602393704).permissions)

@client.event
async def on_message(message):
    if not message.author.bot:
        if "<:hi:975067024256552980>" in message.content:
            await message.channel.send(message.author.mention)
            await message.channel.send("<:hello:1085762478866174072>")

        if "<:hello:1085762478866174072>" in message.content:
            await message.channel.send(message.author.mention)
            await message.channel.send("<:hi:975067024256552980>")

        if "<@920358051893104671> happy birthday" in message.content.lower():
            ssamboHook = await client.fetch_webhook(1083586277510758501) #SSAMBOZOHOOK
            await ssamboHook.send("thanks")

        if "🪞" in message.content and random()<0.01:
            await message.author.timeout(timedelta(hours=1))
            await message.channel.send(f"{message.author.name} won the 1/100 mirror lotto and got timed out!")

        if random() < 1/2**16:
            await message.channel.send(f"{message.author.name} won the <@&1077712282022334474> role!")
            await message.author.add_roles(Snowflake(1077712282022334474)) # SHINY
            print(f"{message.author.id} received the shiny role. ID: {message.id} Channel: {message.channel}")

        if message.author.id == 617541280154517641 and "koru" in message.content.lower(): # the id is ninjayas
            await message.channel.send("Ayo ninjayas why are you saying koru? Everyone knows its kuro smh my head")

        if "rosco sucks" in message.content.lower():
            await message.channel.send("https://cdn.discordapp.com/attachments/921447683846180976/1090785540837756938/image.png") #rosco sucks ss


    # if "<@188217700697243648>" in message.content:
    #   if not message.author.bot:
    #       try:
    #           await message.author.edit(timeout=nextcord.utils.utcnow()+datetime.timedelta(seconds=4233600))
    #       except Exception as e:
    #           await message.channel.send("I can't time you out! Error message: `"+str(e)+"`")
    #       await client.get_channel(926936642181271592).send(f"{message.author.mention} pinging sam")
    #       await client.get_channel(979453104233799740).send(f"https://discord.com/channels/921447683154145331/{message.channel.id}/{message.id}: {message.author.display_name} pinged sam")


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
            `/bracket` - Sends a bracket of some cool players (WIP)
            `/leaderboard` - shows the current Battles 2 leaderboard
            `/user` - Shows information about a user, either by leaderboard position, username, or OakID\n
            ||Created by JazzyJonah - Source code: https://github.com/JazzyJonah/tourney-bot||""")


@client.slash_command(name="trailer", description="The official trailer for B2T", guild_ids=testingServersIDs)
async def trailer(interaction: Interaction):
    if random() < 0.01:
        await interaction.response.send_message("NO, NOW SHUT UP BOZO")
    else:
        await interaction.response.send_message("https://www.youtube.com/watch?v=hn5jQF6KRok")


@client.slash_command(name="map", description="Generate a random HoM map for the tourney", guild_ids=testingServersIDs)
async def map(interaction: Interaction):
    await interaction.response.send_message(choice(["Basalt Columns", "Inflection", "Building Site", "Castle Ruins", "Koru", "Dino Graveyard", "Oasis", "Garden", "Glade", "Ports", "Sands of Time", "Star"]))


@client.slash_command(name="create_tourney", description="Create a tournament! (Mod only)", guild_ids=testingServersIDs)
# Tournament Admin, new role
@application_checks.check_any(application_checks.is_owner(), application_checks.has_any_role(929782523146432562, 845011146552508437))
async def create_tourney(
    interaction: Interaction,
    date_time: str = SlashOption(
        name="date_time",
        description="Date/time (format: MM/DD/YY HH:MM Timezone, eg. 04/16/22 15:45 EST)",
        required=True
    )
):
    if random() < 0.01:
        await interaction.response.send_message("NO, NOW SHUT UP BOZO")
    else:
        try:
            vrej = convert(date_time.rsplit(" ", 1)[0], date_time.split()[-1])
            await interaction.response.send_message("Tournament starts at <t:" + vrej + "> or <t:" + vrej + ":R>")
        except Exception as e:
            await interaction.response.send_message("You messed up somewhere. Try again. (Error message: " + str(e)+")", ephemeral=True)

    # os.remove("bracket.png")


@create_tourney.error
async def on_create_tourney_error(interaction: Interaction, error):
    await interaction.response.send_message("You don't have tournament admin.")


# class Winner(nextcord.ui.View):
#   def __init__(self, player0="", player1=""):
#       super().__init__()
#       self.player0=player0
#       self.player1=player1
#       self.value=None

#   @nextcord.ui.button(label=self.player0, style=nextcord.ButtonStyle.grey)
#   async def player0(self, button:nextcord.ui.button, interaction:Interaction):
#       self.value=self.player0
#       self.stop()

#   @nextcord.ui.button(label=self.player1, style=nextcord.ButtonStyle.grey)
#   async def player0(self, button:nextcord.ui.button, interaction:Interaction):
#       self.value=self.player1
#       self.stop()

@client.slash_command(name="bracket", description="Sends a bracket of some cool players", guild_ids=testingServersIDs)
async def bracket(
    interaction: Interaction,
    player1: nextcord.Member = SlashOption(
        name="player1",
        description="First player",
        required=True
    ),
    player2: nextcord.Member = SlashOption(
        name="player2",
        description="Second player",
        required=True
    ),
    player3: nextcord.Member = SlashOption(
        name="player3",
        description="Third player",
        required=False
    ),
    player4: nextcord.Member = SlashOption(
        name="player4",
        description="Fourth player",
        required=False
    ),
    player5: nextcord.Member = SlashOption(
        name="player5",
        description="Fifth player",
        required=False
    ),
    player6: nextcord.Member = SlashOption(
        name="player6",
        description="Sixth player",
        required=False
    ),
    player7: nextcord.Member = SlashOption(
        name="player7",
        description="Seventh player",
        required=False
    ),
    player8: nextcord.Member = SlashOption(
        name="player8",
        description="Eigth player",
        required=False
    ),
    player9: nextcord.Member = SlashOption(
        name="player9",
        description="Ninth player",
        required=False
    ),
    player10: nextcord.Member = SlashOption(
        name="player10",
        description="Tenth player",
        required=False
    ),
    player11: nextcord.Member = SlashOption(
        name="player11",
        description="Eleventh player",
        required=False
    ),
    player12: nextcord.Member = SlashOption(
        name="player12",
        description="Twefth player",
        required=False
    ),
    player13: nextcord.Member = SlashOption(
        name="player13",
        description="Thirteenth player",
        required=False
    ),
    player14: nextcord.Member = SlashOption(
        name="player14",
        description="Fourteenth player",
        required=False
    ),
    player15: nextcord.Member = SlashOption(
        name="player15",
        description="Fifteenth player",
        required=False
    ),
    player16: nextcord.Member = SlashOption(
        name="player16",
        description="Sixteenth player",
        required=False
    ),

):
    if random() < 0.01:
        await interaction.response.send_message("NO, NOW SHUT UP BOZO")
    else:
        await interaction.response.defer()
        players = []
        if True:  # for collapsing - appends a bunch of stuff to players
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
                                                            players.append(
                                                                    Player(player14.name, player14.display_avatar, 0))
                                                            if player15:
                                                                players.append(
                                                                        Player(player15.name, player15.display_avatar, 0))
                                                                if player16:
                                                                    players.append(
                                                                            Player(player16.name, player16.display_avatar, 0))

        shuffle(players)
        # this is just a length 2 list because threading is dumb - first item is url of imgbb thing, second item is matches for next round
        result = [None, None]
        backgroundBracket = threading.Thread(target=createbracket, name='', args=(
                players, result))  # this is so it doesn't block out nextcord
        backgroundBracket.start()
        while backgroundBracket.is_alive():  # waits until program is finished while not blocking anything
            pass
        await interaction.followup.send(result[0])  # , view=Winner("Heli ice"))
        os.remove("bracket.png")


@client.slash_command(guild_ids=testingServersIDs)
async def user(interaction: Interaction):
    pass


def find_player(season, username=None, oakID=None, page=1):
    if username:
        r = requests.get(f"https://data.ninjakiwi.com/battles2/homs/season_{season-1}/leaderboard?page={page}").json()
        if player := next((x for x in r['body'] if x['displayName'].lower() == username.lower()), False):
            profile = requests.get(player['profile']).json()['body']
            ranks = requests.get(profile['homs']).json()['body'][11-season]
            return profile, ranks
        return find_player(season, username=username, page=page+1)
    elif oakID:
        profile = requests.get(f"https://data.ninjakiwi.com/battles2/users/{oakID}").json()['body']
        ranks = requests.get(f"https://data.ninjakiwi.com/battles2/users/{oakID}/homs").json()['body'][11-season]
        return profile, ranks


@user.subcommand(description="Gets user information based on leaderboard position")
async def leaderboard_position(
    interaction: Interaction,
    LeaderboardPosition: int = SlashOption(
            name="leaderboard_position", description="The position on the leaderboard the user is", required=True),
    Season: int = SlashOption(
            name="season", description="The season that you want to look at (default 11)", required=False)
):
    if interaction.user.id == 1033226573001797712:
        await interaction.response.send_message("Gossy I've done you enough favors", ephemeral=True)
        return
    LeaderboardPosition -= 1
    await interaction.response.defer()
    try:
        if not Season:
            Season = 11
        if Season < 9:
            await interaction.followup.send("Only seasons 9+ are supported, sorry!")
            return
        page = LeaderboardPosition//50+1  # 50 players per page
        endpoint = f"https://data.ninjakiwi.com/battles2/homs/season_{Season-1}/leaderboard?page={page}"
        r = requests.get(endpoint).json()
        player = r['body'][LeaderboardPosition % 50]

        profile = requests.get(player['profile']).json()['body']
        ranks = requests.get(profile['homs']).json()['body'][11-Season]

        result = [None]
        backgroundEmbed = threading.Thread(target=createPlayerEmbed, name='', args=(
                profile, ranks, Season, interaction, result))  # this is so it doesn't block out nextcord
        backgroundEmbed.start()
        while backgroundEmbed.is_alive():  # waits until program is finished while not blocking anything
            pass
        em = result[0]

        await interaction.followup.send(embed=em)
    except Exception as e:
        print(e)
        await interaction.followup.send("An error occured!", ephemeral=True)


        

@user.subcommand(description="Gets user information based on username")
@cooldowns.cooldown(6, 60, bucket=cooldowns.SlashBucket.command)
async def username(
    interaction: Interaction,
    username: str = SlashOption(
            name="username", description="The username of the player on the leaderboard", required=True),
    season: int = SlashOption(
            name="season", description="The season that you want to  look at (only seasons 9+ are supported)", required=False)
):
    if interaction.user.id == 1033226573001797712:
        await interaction.response.send_message("Gossy I've done you enough favors", ephemeral=True)
        return
    await interaction.response.defer()
    try:
        if not season:
            season = 11

        

        profile, ranks = find_player(season, username=username)
        result = [None]
        backgroundEmbed = threading.Thread(target=createPlayerEmbed, name='', args=(
                profile, ranks, season, interaction, result))
        backgroundEmbed.start()
        while backgroundEmbed.is_alive():
            pass
        em = result[0]

        await interaction.followup.send(embed=em)

    except Exception as e:
        print(e)
        await interaction.followup.send("An error occured! Check for any typos!")

@user.subcommand(description="Gets user information based on OAK ID")
async def oak_id(
    interaction: Interaction,
    oakID: str = SlashOption(
        name="oak_id", description="The OAK ID of the player", required=True),
    season: int = SlashOption(
        name="season", description="The season that you want to look at (only seasons 9+ are supported)", required=False)
):
    if interaction.user.id == 1033226573001797712:
        await interaction.response.send_message("Gossy I've done you enough favors", ephemeral=True)
        return
    await interaction.response.defer()
    try:
        if not season:
            season = 11
        profile, ranks = find_player(season, oakID=oakID)
        result = [None]
        backgroundEmbed = threading.Thread(target=createPlayerEmbed, name='', args=(
                profile, ranks, season, interaction, result))
        backgroundEmbed.start()
        while backgroundEmbed.is_alive():
            pass
        em = result[0]

        await interaction.followup.send(embed=em)

    except Exception as e:
        print(e)
        await interaction.followup.send("An error occured! Check for any typos!") 




# @client.event
# async def on_application_command_error(interaction: Interaction, error):
#     await interaction.followup.send("This command is being used too quickly! Try again in a minute.", ephemeral=True)


class WideButton(nextcord.ui.Button):
    def __init__(self, i, page, numPages, totalPlayers, interaction, season):
        label = f"{(i-1)*10+1}-{min([i*10,totalPlayers])}"
        style = nextcord.ButtonStyle.gray if i == page else nextcord.ButtonStyle.blurple
        super().__init__(label=label, style=style)
        self.i = i
        self.page = page
        self.numPages = numPages
        self.totalPlayers = totalPlayers
        self.interaction = interaction
        self.season=season

    async def callback(self, interaction: Interaction):
        result = [None]
        backgroundEmbed = threading.Thread(target=createLeaderboardEmbed, name='', args=(self.i, self.season, self.interaction, result))
        backgroundEmbed.start()
        buttons = PageButtons(page=self.i, numPages = self.numPages, totalPlayers = self.totalPlayers, interaction = self.interaction, season = self.season)
        while (backgroundEmbed.is_alive()):
            pass
        em = result[0]

        await interaction.response.edit_message(embed = em, view = buttons)
        await buttons.wait()

# class TallButton(nextcord.ui.Button):
#     def __init__(self, page, numPages, totalPlayers, authorID, season):

class PageButtons(nextcord.ui.View):
    def __init__(self, page, numPages, totalPlayers, interaction, season):
        super().__init__()
        self.page = page
        self.value = None
        self.numPages = numPages
        self.interaction = interaction

        for i in range(1, numPages+1):
            button = WideButton(i, self.page, self.numPages, totalPlayers, interaction, season)
            try:
                self.add_item(button)
            except:
                pass
    async def interaction_check(self, interaction: Interaction):
        if interaction.user.id == self.interaction.user.id:
            return True
        else:
            await interaction.response.send_message("You do not have permission to use this.", ephemeral=True)
            return False









@client.slash_command(name = "leaderboard", description = "Shows the current leaderboard", guild_ids = testingServersIDs)
async def leaderboard(interaction:Interaction, 
    page: int = SlashOption(name = "page", description = "The set of 10 you want to look at", required = False),
    season: int = SlashOption(name = "season", description = "The season that you want to look at (only seasons 9+ are supported)", required = False)
):
    if interaction.user.id == 1033226573001797712:
        await interaction.response.send_message("Gossy I've done you enough favors", ephemeral=True)
        return
    await interaction.response.defer()
    try:
        if not season:
            season = 11
        if page: # A lot easier -- update: ok maybe not
            result = [None]
            backgroundEmbed = threading.Thread(target = createLeaderboardEmbed, name = '', args = (page, season, interaction, result))
            backgroundEmbed.start()
            while(backgroundEmbed.is_alive()):
                pass
            em = result[0]

            await interaction.followup.send(embed = em)
        else: #the real pain
            page = 1
            result = [None]
            backgroundEmbed = threading.Thread(target = createLeaderboardEmbed, name = '', args = (1, season, interaction, result))
            backgroundEmbed.start()
            while(backgroundEmbed.is_alive()):
                pass
            em = result[0]

            totalPlayers=requests.get("https://data.ninjakiwi.com/battles2/homs/").json()["body"][11-season]["totalScores"]
            buttons = PageButtons(page=1, numPages = totalPlayers//10+1, totalPlayers = totalPlayers, interaction = interaction, season = season)
            await interaction.followup.send(embed = em, view = buttons)
            await buttons.wait()

    except Exception as e:
        print(e)
        await interaction.followup.send("An error occured! Fix it, or else...", ephemeral=True)





# @client.slash_command(name = "testing", description="vrej", guild_ids=testingServersIDs)
# async def testing(interaction:Interaction):
#   embed = nextcord.Embed(title = "Viby", description = "vrej")
#   embed.set_thumbnail("https://static-api.nkstatic.com/appdocs/4/assets/opendata/641e8696f4b80d78280c769cc06c53f4_mastery_science_gwen_avatar.png?pretty=true")
#   embed.add_field(name = "wins", value = "5\n4\n3", inline = True) #This works
#   embed.add_field(name="Losses", value = "4", inline = True)
#   embed.add_field(name="score", value = "3501", inline = True)
#   embed.add_field(name = "winStreak", value = "8", inline = True)
#   await interaction.response.send_message(embed = embed)






# @client.slash_command(name="leaderboard", description="Sends the t10 current players in Battles 2!", guild_ids=testingServersIDs)
# async def leaderboard(interaction:Interaction):
#   import requests
#   import json
#   r=requests.get("https://fast-static-api.nkstatic.com/storage/static/appdocs/17/leaderboards/lb:hom_rank:season_8:public.json", headers={"user-agent":"battles2-1.7.2"}, data={"key":"value"})
#   r.json()
#   data = json.loads(json.loads(r.text)['data'])
#   message=""
#   for i in range(10):
#       try:
#           message+=f'#{i+1}: {getPlayerMap()[data["scores"]["equal"][i]["userID"]]}\n'
#       except:
#           message+=f'#{i+1}: unknown\n'
#   await interaction.response.send_message("```"+message+"```")


if os.getenv("token")!= None:
    client.run(os.getenv("token"))
else:
    client.run(tokenSucks())