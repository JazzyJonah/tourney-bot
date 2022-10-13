from diagrams import Cluster, Diagram
from diagrams.generic.blank import Blank
from diagrams.custom import Custom
from imgFromURL import getimage
from random import choice
import os
from os.path import exists


def createbracket(p1, p1av, p2, p2av, p3, p3av, p4, p4av):
    p1 = (p1, p1av)
    p2 = (p2, p2av)
    p3 = (p3, p3av)
    p4 = (p4, p4av)
    players = [p1, p2, p3, p4]

    with Diagram("bracket", show=False):
        with Cluster("Round 1"):
            g1p1 = Custom(players[0][0], getimage(players[0][1]))
            g1p2 = Custom(players[1][0], getimage(players[1][1]))
            g1p3 = Custom(players[2][0], getimage(players[2][1]))
            g1p4 = Custom(players[3][0], getimage(players[3][1]))
        with Cluster("Finals"):
            players = [choice(players[0:2]), choice(players[2:4])]
            g2p1 = Custom(players[0][0], getimage(players[0][1]))
            Blank("")
            g2p2 = Custom(players[1][0], getimage(players[1][1]))
        with Cluster("Winner"):
            winner = Custom(players[1][0], getimage(players[1][1]))
        [g1p1, g1p2] >> g2p1 >> winner
        [g1p3, g1p4] >> g2p2 >> winner
    i=0
    while exists("temp.png"+str(i)):
        os.remove("temp.png"+str(i))
        i+=1

