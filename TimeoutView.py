from nextcord import Interaction
from nextcord.abc import Snowflake
import nextcord
from datetime import timedelta
from updateLBTxt import updateLBTxt


class TimeoutView(nextcord.ui.View):
    def __init__(self, client):
        super().__init__(timeout=None)
        self.client = client

    @nextcord.ui.button(label="Timeout", style=nextcord.ButtonStyle.red, custom_id="e")
    async def clicked(self, button: nextcord.ui.Button, interaction: Interaction):
        try:
            await interaction.user.timeout(timedelta(minutes=5))
            updateLBTxt(interaction)
            with open("buttonLB.txt") as f:
                data = f.readlines()

            def epic_sort(item):
                return int(item.split(" ")[1])
            data.sort(key=epic_sort, reverse=True)

            em = nextcord.Embed(title="Timeout Leaderboard", url="https://discord.com/channels/921447683154145331/921456054435455133/1091455632915308697", color=int("F1C40F", 16))  # big red button link, shiny color

            users = ""
            timeouts = ""
            for i in range(min(10, len(data))):
                userID = int(data[i].split(" ")[0])
                # adds the username to the users list
                user = await self.client.fetch_user(userID)
                users += user.display_name + "\n"
                # adds timeouts to timeouts list
                timeouts += data[i].split(" ")[1] + "\n"

            em.add_field(name="Username", value=users, inline=True)
            em.add_field(name="# Timeouts", value=timeouts, inline=True)


            channel = self.client.get_channel(1091916069595271208)
            message = await channel.fetch_message(1091916387498340373)

            await message.edit(content = "", embed=em) 
            
            #channel is timeoutlb, message is the leaderboard itself. why its like this? idk.
            # the reason i couldnt put that into a function is because of dumb await stuff

            if random()<5/2**13:
                await interaction.user.add_roles(Snowflake(1077712282022334474)) # SHINY
                await interaction.response.send_message("YOU GOT THE SHINY ROLE", ephemeral=True)
                await self.client.get_channel(921447683846180976).send(f"{interaction.user.name} clicked the big red button... AND BECAME SHINY")


            else:
                await interaction.response.send_message("You've been timed out. GG", ephemeral=True)
                await self.client.get_channel(1029501175009116200).send(f"{interaction.user.name} clicked the big red button.")
           
        except Exception as e:
            await interaction.response.send_message(f"{interaction.user.name} shut up", ephemeral=True)
            #print(e)