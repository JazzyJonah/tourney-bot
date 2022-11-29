from diagrams import Cluster, Diagram
from diagrams.gcp.analytics import BigQuery, DataFlow, PubSub
from diagrams.generic.blank import Blank
from diagrams.custom import Custom
import random
from random import shuffle
import os
from math import floor, log, ceil
import requests
import shutil
from os.path import exists
from player import Player, getimage



def subtract(lst1, lst2):
    return [x for x in lst2 if x not in lst1]

# def find_instance(list, value, index):
#     return [z for z, n in enumerate(list) if n == value][index]

def len_group(numPlayers, group):
    return 2**ceil(log(numPlayers, 2))-1-2*(group-1)



def createbracket(players):
    question="https://www.citypng.com/public/uploads/small/11664478536ju7umc1lgtvjg5pkqxzszbnnsiidksg2azldiuudv5lm2m4qjror6fwyabkot9ludlybku4g1pptb3qxm1sosuj55vtdldgrtyqu.png"
    for i in range(len(players)):
        players[i] = Player(players[i][0], players[i][1], players[i][2])
    numPlayers = len(list(players))
    n = floor(log(numPlayers, 2))
    k = numPlayers - 2**n
    group1 = []
    powerOf2 = log(numPlayers, 2).is_integer()
    if powerOf2:
        group1 = players
    else:
        for i in range(2*k):
            group1.append(players[i])
        group2 = subtract(group1, players)

        while group2.count(False) < k:
            group2.insert(group2.count(False)*2+1, False)


    with Diagram("bracket", show=False):
        if powerOf2:
            with Cluster("group 1"):
                actualGroup1=[]
                for i in range(len(group1)):
                    actualGroup1.append(group1[i].make_box())

            #PAST ROUND 2
            newGroups=int(log(len(group1), 2))
            futureGroups=[]
            actualFutureGroups=[]
            for i in range(newGroups):
                with Cluster("group "+str(2+i)):
                    futureGroups.append([])
                    actualFutureGroups.append([])
                    if i == 0:
                        currentPlayers=int(len(group1)/2)
                    else:
                        currentPlayers=int(len(futureGroups[i-1])/2)#(2**(i+1)))
                    numBlanks = len_group(numPlayers, 1+i)-currentPlayers


                    if i==0:
                        for j in range(int(len(actualGroup1)/2)):
                            try:
                                winner=random.choice([group1[2*j], group1[2*j+1]])
                                futureGroups[i].append(winner)
                                actualFutureGroups[i].append(winner.make_box())
                                # if group1[2*j].get_wins() > group1[2*j+1].get_wins():
                                #     futureGroups[i].append(group1[2*j])
                                #     actualFutureGroups[i].append(group1[2*j].make_box())
                                
                                # elif group1[2*j].get_wins() < group1[2*j+1].get_wins():
                                #     futureGroups[i].append(group1[2*j+1])
                                #     actualFutureGroups[i].append(group1[2*j+1].make_box())
                                
                                # elif group1[2*j].get_wins() == group1[2*j+1].get_wins():
                                #     futureGroups[i].append(False)
                                #     actualFutureGroups[i].append(Custom("", getimage(question)))

                            except Exception as e:
                                futureGroups[i].append(False)
                                actualFutureGroups[i].append(Custom("", getimage(question)))


                            if j!=int(len(actualGroup1)/2-1):
                                for k in range(int(numBlanks/(currentPlayers-1))):
                                    Blank("")
                    else:
                        for j in range(int(len(actualFutureGroups[i-1])/2)):
                            try:
                                winner=random.choice([futureGroups[i-1][2*j], futureGroups[i-1][2*j+1]])
                                futureGroups[i].append(winner)
                                actualFutureGroups[i].append(winner.make_box())
                                # if futureGroups[i-1][2*j].get_wins() > futureGroups[i-1][2*j+1].get_wins():
                                #     futureGroups[i].append(futureGroups[i-1][2*j])
                                #     actualFutureGroups[i].append(futureGroups[i-1][2*j].make_box())

                                # elif futureGroups[i-1][2*j].get_wins() < futureGroups[i-1][2*j+1].get_wins():
                                #     futureGroups[i].append(futureGroups[i-1][2*j+1])
                                #     actualFutureGroups[i].append(futureGroups[i-1][2*j+1].make_box())

                                # elif futureGroups[i-1][2*j].get_wins() == futureGroups[i-1][2*j+1].get_wins():
                                #     futureGroups[i].append(False)
                                #     actualFutureGroups[i].append(Custom("", getimage(question)))
                            except:
                                futureGroups[i].append(False)
                                actualFutureGroups[i].append(Custom("", getimage(question)))

                            if j!=int(len(actualFutureGroups[i-1])/2-1):
                                if currentPlayers!=1:
                                    for k in range(int(numBlanks/(currentPlayers-1))):
                                        Blank("")

                if i==0:
                    for j in range(int(len(actualGroup1)/2)):
                        [actualGroup1[2*j], actualGroup1[2*j+1]] >> actualFutureGroups[0][j]
                else:
                    for j in range(int(len(futureGroups[i-1])/2)):
                        [actualFutureGroups[i-1][2*j], actualFutureGroups[i-1][2*j+1]] >> actualFutureGroups[i][j]








        else:
            with Cluster("group 2"):
                actualGroup2=[]
                g2len=0
                l=0
                for i in range(len(group2)):
                    if group2[i]:
                        actualGroup2.append(group2[i].make_box())
                        group2[i].win()
                        g2len+=1
                    else:
                        winner=random.choice([group1[2*l], group1[2*l+1]])
                        group2[i]=winner
                        actualGroup2.append(winner.make_box())
                        # if group1[2*l].get_wins()>group1[2*l+1].get_wins():
                        #     group2[i] = group1[2*l]#group2.append(group1[2*l])
                        #     actualGroup2.append(group1[2*l].make_box())
                        # elif group1[2*l].get_wins()<group1[2*l+1].get_wins():
                        #     group2[i] = group1[2*l+1]#group2.append(group1[2*l+1])
                        #     actualGroup2.append(group1[2*l+1].make_box())
                        # else:
                        #     actualGroup2.append(Custom("", getimage(question)))
                        l+=1
                    if i<(len(group2)-1):
                        Blank("")

            actualGroup1=[]
            with Cluster("group 1"):
                l=g2len
                for i in range(int(len(group1)/2)):
                    if l!=0 and i!=0:
                        # for j in range(2):
                        #     Blank("")
                        l-=1
                    actualGroup1.append(group1[2*i].make_box())
                    actualGroup1.append(group1[2*i+1].make_box())
            for i in range(k):
                if g2len > 0:
                    [actualGroup1[2*i], actualGroup1[2*i+1]] >> actualGroup2[2*i+1]
                    g2len -= 1
                    x=i+1
                else:
                    [actualGroup1[2*i], actualGroup1[2*i+1]] >> actualGroup2[x+i]


            #PAST ROUND 2
            newGroups=int(log(len(group2), 2))
            futureGroups=[]
            actualFutureGroups=[]
            for i in range(newGroups):
                with Cluster("group "+str(3+i)):
                    futureGroups.append([])
                    actualFutureGroups.append([])
                    currentPlayers=int(len(group2)/(2**(i+1)))
                    numBlanks = len_group(numPlayers, 2+i)-currentPlayers


                    if i==0:
                        for j in range(int(len(actualGroup2)/2)):
                            try:
                                winner=random.choice([group2[2*j], group2[2*j+1]])
                                futureGroups[i].append(winner)
                                actualFutureGroups[i].append(winner.make_box())
                                # if group2[2*j].get_wins() > group2[2*j+1].get_wins():
                                #     futureGroups[i].append(group2[2*j])
                                #     actualFutureGroups[i].append(group2[2*j].make_box())
                                
                                # elif group2[2*j].get_wins() < group2[2*j+1].get_wins():
                                #     futureGroups[i].append(group2[2*j+1])
                                #     actualFutureGroups[i].append(group2[2*j+1].make_box())
                                
                                # elif group2[2*j].get_wins() == group2[2*j+1].get_wins():
                                #     futureGroups[i].append(False)
                                #     actualFutureGroups[i].append(Custom("", getimage(question)))

                            except Exception as e:
                                futureGroups[i].append(False)
                                actualFutureGroups[i].append(Custom("", getimage(question)))


                            if j!=int(len(actualGroup2)/2-1):
                                for k in range(int(numBlanks/(currentPlayers-1))):
                                    Blank("")
                    else:
                        for j in range(int(len(actualFutureGroups[i-1])/2)):
                            try:
                                winner=random.choice([futureGroups[i-1][2*j], futureGroups[i-1][2*j+1]])
                                futureGroups[i].append(winner)
                                actualFutureGroups[i].append(winner.make_box())
                                # if futureGroups[i-1][2*j].get_wins() > futureGroups[i-1][2*j+1].get_wins():
                                #     futureGroups[i].append(futureGroups[i-1][2*j])
                                #     actualFutureGroups[i].append(futureGroups[i-1][2*j].make_box())

                                # elif futureGroups[i-1][2*j].get_wins() < futureGroups[i-1][2*j+1].get_wins():
                                #     futureGroups[i].append(futureGroups[i-1][2*j+1])
                                #     actualFutureGroups[i].append(futureGroups[i-1][2*j+1].make_box())

                                # elif futureGroups[i-1][2*j].get_wins() == futureGroups[i-1][2*j+1].get_wins():
                                #     futureGroups[i].append(False)
                                #     actualFutureGroups[i].append(Custom("", getimage(question)))
                            except:
                                futureGroups[i].append(False)
                                actualFutureGroups[i].append(Custom("", getimage(question)))

                if i==0:
                    for j in range(int(len(actualGroup2)/2)):
                        [actualGroup2[2*j], actualGroup2[2*j+1]] >> actualFutureGroups[0][j]
                else:
                    for j in range(int(len(futureGroups[i-1])/2)):
                        [actualFutureGroups[i-1][2*j], actualFutureGroups[i-1][2*j+1]] >> actualFutureGroups[i][j]







    i=0
    while exists("temp"+str(i)+".png"):
        os.remove("temp"+str(i)+".png")
        i+=1

createbracket(
    [("black square1", "https://lh3.googleusercontent.com/9tdJGxGMuvgof_Jh0SFU7r423bKuMIP9wSnOu-sy5RffCwlhBYvugvXfUz-xhpsCfg=h36", 0),
    ("black square2", "https://lh3.googleusercontent.com/9tdJGxGMuvgof_Jh0SFU7r423bKuMIP9wSnOu-sy5RffCwlhBYvugvXfUz-xhpsCfg=h36", 0),
    ("black square3", "https://lh3.googleusercontent.com/9tdJGxGMuvgof_Jh0SFU7r423bKuMIP9wSnOu-sy5RffCwlhBYvugvXfUz-xhpsCfg=h36", 0),
    ("black square4", "https://lh3.googleusercontent.com/9tdJGxGMuvgof_Jh0SFU7r423bKuMIP9wSnOu-sy5RffCwlhBYvugvXfUz-xhpsCfg=h36", 0),
    ("black square5", "https://lh3.googleusercontent.com/9tdJGxGMuvgof_Jh0SFU7r423bKuMIP9wSnOu-sy5RffCwlhBYvugvXfUz-xhpsCfg=h36", 0),
    ("black square5", "https://lh3.googleusercontent.com/9tdJGxGMuvgof_Jh0SFU7r423bKuMIP9wSnOu-sy5RffCwlhBYvugvXfUz-xhpsCfg=h36", 0),
    ("black square6", "https://lh3.googleusercontent.com/9tdJGxGMuvgof_Jh0SFU7r423bKuMIP9wSnOu-sy5RffCwlhBYvugvXfUz-xhpsCfg=h36", 0),
    ("black square7", "https://lh3.googleusercontent.com/9tdJGxGMuvgof_Jh0SFU7r423bKuMIP9wSnOu-sy5RffCwlhBYvugvXfUz-xhpsCfg=h36", 0)]
)