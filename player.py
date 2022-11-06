from diagrams import Cluster, Diagram
from diagrams.gcp.analytics import BigQuery, DataFlow, PubSub
from diagrams.generic.blank import Blank
from diagrams.custom import Custom
from os.path import exists
import requests
import shutil

def getimage(url):
    i=0
    while exists("temp"+str(i)+".png"):
        i+=1
    with open("temp"+str(i)+".png", "wb") as f:
        shutil.copyfileobj(requests.get(url, stream=True).raw, f)
    return "temp"+str(i)+".png"

class Player:
	def __init__(self, name, pfp, wins = 0):
		self.name=name
		self.pfp=pfp
		self.wins=wins
	def get_name(self):
		return self.name
	def get_pfp(self):
		return self.species
	def get_wins(self):
		return self.wins

	def win(self):
		self.wins+=1
	def make_box(self):
		 return Custom(self.name, getimage(self.pfp))

	def __str__(self):
		return f"Name: {self.get_name()}"#\nWins: {self.get_wins()}\n"
	def __repr__(self):
		return self.__str__()
