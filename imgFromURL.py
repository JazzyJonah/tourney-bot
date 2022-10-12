import requests
import shutil
from os.path import exists

def getimage(url):
	i=0
	while exists("temp.png"+str(i)):
		i+=1
	with open("temp.png"+str(i), "wb") as f:
		shutil.copyfileobj(requests.get(url, stream=True).raw, f)
	return "temp.png"+str(i)