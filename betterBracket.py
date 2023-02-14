from PIL import Image, ImageDraw, ImageFont
from urllib.request import urlopen
import numpy
from math import *
import imgbbpy

import requests
import shutil
from tokenSucks import imgbbSucks


class Player:
    def __init__(self, name, pfp, wins=0):
        self.name = name
        self.pfp = pfp
        self.wins = wins
        self.font = ImageFont.truetype("ggsans-Bold.ttf", 50)

    def get_name(self):
        return self.name

    def get_pfp(self):
        return self.species

    def get_wins(self):
        return self.wins

    def win(self):
        self.wins += 1

    def make_box(self):
        base = Image.new("RGBA", (384, 200))
        base.paste(getimage(self.pfp).resize((128, 128)), (128,0))
        draw = ImageDraw.Draw(base)
        w = draw.textbbox((0, 128), self.name, font=self.font)[2]
        draw.text((int((128-w)/2)+128, 128), self.name, font=self.font)
        return base

    def __str__(self):
        return f"Name: {self.get_name()}"  # \nWins: {self.get_wins()}\n"

    def __repr__(self):
        return self.__str__()


def getimage(url):
    with open("temp.png", "wb") as f:
        shutil.copyfileobj(requests.get(url, stream=True).raw, f)
    return Image.open("temp.png")


def draw_line(im, point1, point2, color='white'):
    ImageDraw.Draw(im).line(
        [point1, ((point2[0]+point1[0])/2, point1[1])], fill=color, width=3)
    ImageDraw.Draw(im).line([((point2[0]+point1[0])/2, point1[1]),
                             ((point2[0]+point1[0])/2, point2[1])], fill=color, width=3)
    ImageDraw.Draw(im).line(
        [((point2[0]+point1[0])/2, point2[1]), point2], fill=color, width=3)
    return im


def order_tuples(tuple1, tuple2):
    return [(min([tuple1[0], tuple2[0]]), min([tuple1[1], tuple2[1]])), (max([tuple1[0], tuple2[0]]), max([tuple1[1], tuple2[1]]))]


def draw_arc(im, point1, point2, color):
    midpoint = (int((point2[0]+point1[0])/2), int((point2[1]+point1[1])/2))
    xDelta = point2[0]-point1[0]
    yDelta = point2[1]-point1[1]
    n = 0
    if (point2[1] < point1[1]):
        n = 90
    ImageDraw.Draw(im).arc(order_tuples(
        (midpoint[0]-xDelta, point2[1]), (midpoint[0], point1[1])), -90+n, 0+n, fill=color, width=8)
    ImageDraw.Draw(im).arc(order_tuples(
        (midpoint[0]-4, point2[1]), (midpoint[0]+xDelta, point1[1])), 90+n, 180+n, fill=color, width=8)
    return im


def subtract(lst1, lst2):
    return [x for x in lst2 if x not in lst1]


def instance(value, list, index):
    return [i for i, n in enumerate(list) if n == value][index]


def createbracket(players, returner):
    question = Image.open("question.png").resize((128, 128))
    numPlayers = len(list(players))
    n = floor(log(numPlayers, 2))  # number of groups except the first
    k = numPlayers - 2**n  # how many matches are in r1
    if k == 0:  # power of 2
        k = numPlayers//2  # // is ok because it must be even
    group1 = []
    for i in range(2*k):
        group1.append(players[i])
    group2 = subtract(group1, players)
    # this is the amount of blank spots there should be
    while group2.count(False) < k:
        # in g2 such that each match in g1 matches to False
        group2.insert(group2.count(False)*2+1, False)
    # creating the image n' stuff
    base = Image.new(
        "RGBA", (128*(2*n+3), 128*(2*max([len(group1), len(group2)*2]))))
    # Horizontally it's the width of a box for each group, with blank space between each group and margins
    # Vertically it's the max group with same as above. Might remove margins later

    # building group2 first
    for i in range(len(group2)):
        if not group2[i]:
            base.paste(question, (3*128, 128+512*i))
            continue
        group2[i].win()
        box = group2[i].make_box()
        # x is constant, y is based on its position, i think
        base.paste(box, (2*128, 128+512*i))
    # building group 1
    for i in range(k):
        goal = instance(False, group2, i)
        box1 = group1[i*2].make_box()
        box2 = group1[i*2+1].make_box()
        base.paste(box1, (0, 512*goal))
        base.paste(box2, (0, 256+512*(goal)))
        # draw arcs from box to box
        base = draw_arc(base, (256, 512*goal+64),
                        (3*128, 192+512*goal), color='white')
        base = draw_arc(base, (256, 256+512*goal+64),
                        (3*128, 192+512*goal), color='white')
    # DO THE REST!
    remainingGroups = []
    for i in range(n): # why its n and not n-1? i have *no* idea
        remainingGroups.append([])
        if i == 0:  # third group, gotta look at second group for this one
            # this is making the next entry in remainingGroups
            for j in range(len(group2)//2):
                if group2[2*j] and group2[2*j+1]:
                    if group2[2*j].get_wins() > group2[2*j+1].get_wins():
                        remainingGroups[i].append(group2[2*j])
                    elif group2[2*j+1].get_wins() > group2[2*j].get_wins():
                        remainingGroups[i].append(group2[2*j+1])
                    else:
                        remainingGroups[i].append(False)
                else:
                    remainingGroups[i].append(False)
                # this is kinda a different section but including it in same loop for *efficiency*
                # these are drawing arcs from the previous group to the current one
                base = draw_arc(base, (4*128, 192+j*2*512),
                                (5*128, 448+j*2*512), color='white')
                base = draw_arc(base, (4*128, 192+(j*2+1)*512),
                                (5*128, 448+j*2*512), color='white')
        else:
            for j in range(len(remainingGroups[i-1])//2):
                if remainingGroups[i-1][2*j] and remainingGroups[i-1][2*j+1]:
                    if remainingGroups[i-1][2*j].get_wins() > remainingGroups[i-1][2*j+1].get_wins:
                        remainingGroups[i].append(group2[2*j])
                    elif remainingGroups[i-1][2*j+1].get_wins() > remainingGroups[i-1][2*j].get_wins():
                        remainingGroups[i].append(group2[2*j+1])
                    else:
                        remainingGroups[i].append(False)
                else:
                    remainingGroups[i].append(False)
                # again, kinda different, but efficiency
                # these are drawing arcs from the previous group to the current one
                base = draw_arc(base, ((4+i*2)*128, 256*2**i-64 + j*2 * 2**i*512),
                                ((5+i*2)*128, 2**i*512-256+2**i*512*j*2+192), color='white')
                base = draw_arc(base, ((4+i*2)*128, 256*2**i-64 + (j*2+1) * 2**i*512),
                                ((5+i*2)*128, 2**i*512-256+2**i*512*j*2+192), color='white')
                # print(((4+i*2)*128, 192*2**i + (j*2+1) * 2**i*256),((5+i*2)*128, 192*2**i + (j*2 * 2**i*256)//2))
            # drawing the pictures
        for j in range(len(remainingGroups[i])):
            if not remainingGroups[i][j]:
                base.paste(question, (128+256*(i+2), 2**i*512-128 + 2**i*512*j*2))
            else:
                base.paste(remainingGroups[i][j].make_box(), (256*(i+2), 2**i*512-128 + 2**i*512*j*2))

    base.save("bracket.png")
    returner[0] = imgbbpy.SyncClient(imgbbSucks()).upload(file='bracket.png').url
    # base.show()

    ## returns players that still have to play
    #do the above
    returner[1] = ['foo', 'bar']


# createbracket(
#     [
#         Player("black", "https://creazilla-store.fra1.digitaloceanspaces.com/emojis/45970/black-medium-small-square-emoji-clipart-xl.png"),
#         Player("red", "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSn2NrOEh3YmYVL8AXia6PS3veLnOH1j5me0mImkceC_ZcSLXcDPLUbL_SAc41jOzwhtIc&usqp=CAU"),
#         Player("blue", "https://emojipedia-us.s3.amazonaws.com/source/microsoft-teams/337/large-blue-square_1f7e6.png"),
#         Player("green", "https://pixy.org/src/48/483923.png"),
#         Player("orange", "https://www.emoji.com/wp-content/uploads/filebase/icons/emoji-icon-glossy-25-33-symbols-geometric-orange-square-72dpi-forPersonalUseOnly.png"),
#         Player("purple", "https://emojipedia-us.s3.amazonaws.com/source/microsoft-teams/337/large-purple-square_1f7ea.png"),
#         Player("white", "https://www.meme-arsenal.com/memes/0ba23837b415094e327821ea7e769775.jpg"),
#         Player("cyan", "https://images.squarespace-cdn.com/content/v1/5900edd04402437eea15e59e/1498941169560-8PGH0QC94YK9QNA7ALQ1/image-asset.png"),
#         Player("magenta", "https://bookshow.blurb.com/bookshow/cache/P9202979/md/cover_2.jpeg?access_key=6360452ccc88a529066287863df92f80")
#     ]
# )


# COOL THINGS YOU COULD DO, HYPOTHETICALLY:
# im = Image.open('Untitled drawing.png')
# print(im.format, im.size, im.mode)
# im.show()
# croppedIm = im.crop((topLeftX, topLeftY, bottomRightX, bottomRightY))
# im.save('Untitled drawing2.png') # creates a new file, doesn't rename an old one
# rotatedIm = im.rotate(45) # degrees counterclockwise
# im.paste(otherIm, (topLeftX, topLeftY)) # If there's no position tuple, it'll default to top left
# im.paste(otherIm, (0,0), 122.5) # half transparent
# r, g, b, a = drawing.split() # split returns 3 (ig 4 but alpha doesnt count) images with each having its rgb color of each pixel becoming the value in every rgb color
# # a pixel thats (3,34,5) in the og image will be (3,3,3) in r, (34,34,34) in g, (5,5,5) in b
# reversedIm = Image.merge("RGB",(b,g,r)) # in total this swapped r and b
# biggerIm = im.resize((1000,1000))
# filteredIm = im.filter(PIL.ImageFilter.DETAIL) # ye idk what this does either
# brighterIm = im.point(function) # function would take in one argument and return it times some number to actually brighten it
# im.putpixel((x, y), (255, 0, 0)) #coord, rgb val
# def draw_line(im, point1, point2, color):
# 	slope = (point1[1]-point2[1])/(point2[0]-point1[0])
# 	n=1
# 	if -1<slope<1: ## HORIZONTAL
# 		if numpy.abs(point2[0]-point1[0]) != point2[0]-point1[0]:
# 			n=-1
# 		for i in range(numpy.abs(point2[0]-point1[0])):
# 			for j in range(3):
# 				for k in range(3):
# 					im.putpixel((point1[0]+n*i+j, point1[1]-int(n*i*slope)+k), color)

# 	if slope<-1 or slope>1: ## VERTICAL
# 		if numpy.abs(point2[1]-point1[1]) != point2[1]-point1[1]:
# 			n=-1
# 		for i in range(numpy.abs(point2[1]-point1[1])):
# 			for j in range(3):
# 				for k in range(3):
# 					im.putpixel((point1[0]-int(n*i*1/slope)+j, point1[1]+n*i+k), color)

# 	return im
# pfp = getimage("https://cdn.discordapp.com/avatars/627917067332485120/195cb543f9006e9024401fe3d6a871cc.png") # 128x128
# im = Image.new("RGBA",(1000,1000))
# im = draw_arc(im, (100,450), (900,500), (255,255,255))
# im = draw_arc(im, (100,550), (900,500), (255,255,255))
# im.show()
# im.save('line.png')
