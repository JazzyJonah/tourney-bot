from diagrams import Cluster, Diagram
from diagrams.gcp.analytics import BigQuery, DataFlow, PubSub
import random
def bracket():
    p1 = "a"
    p2 = "b"
    p3 = "c"
    p4 = "d"
    players = ["a", "b", "c", "d"]

    with Diagram("bracket"):
        with Cluster("Round 1"):
            g1p1 = PubSub(players[0])
            g1p2 = PubSub(players[1])
            g1p3 = PubSub(players[2])
            g1p4 = PubSub(players[3])
        with Cluster("Finals"):
            players = [random.choice(players[0:2]), random.choice(players[2:4])]
            g2p1 = PubSub(players[0])
            g2p2 = PubSub(players[1])
        with Cluster("Winner"):
            winner = PubSub(random.choice(players))
        [g1p1, g1p2] >> g2p1 >> winner
        [g1p3, g1p4] >> g2p2 >> winner