def updateLBTxt(interaction):
    with open("C:/Users/jonah/Documents/GitHub/tourney-bot/buttonLB.txt") as f:
        data = f.readlines()
        players = [int(line.split(" ")[0]) for line in data] # all the players on the lb
        print(players)
        print(interaction.user.id)
        if interaction.user.id in players:
            x=players.index(interaction.user.id)
            data[x] = f"{interaction.user.id} {int(data[x].split(' ')[1])+1} \n" # extra space at the end is to prevent newline from getting in the way
        else:
            data.append(f"{interaction.user.id} 1 \n")
    f.close()

    with open("C:/Users/jonah/Documents/GitHub/tourney-bot/buttonLB.txt", "w") as f:
        f.writelines(data)