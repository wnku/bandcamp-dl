import argparse as ap
import requests
import re
import urllib.request
import shutil
from lxml import html
import os

request_header = {
    'User-Agent': "Mozilla/5.0 (X11; Linux x86_64; rv:12.0) Gecko/20100101 Firefox/12.0"
}


audioRegex = r"(https:\/\/t4.bcbits.com\/stream\/[a-z0-9]{32}\/mp3-128\/[0-9]{10}\?p=[0-9]&ts=[0-9]{10}&t=[a-z0-9]{40}&token=[0-9]{10}_[a-z0-9]{40})"
titleRegex = r"(\n............)(.*)(\n............)(\n........)"
userRegex = r"(\/\/)(.*)(\.bandcamp\.com)"

titleXpath = '//*[@id="name-section"]/h2/text()'
albumXpath = '//*[@id="name-section"]/h3/span[1]/a/span/text()'

directoryPath = "D:\\Music Archive\\Bandcamp\\"

def directoryExists(directoryPath): # Checks whether directory exists. A utility for downloadLog().
    directory = os.path.dirname(directoryPath)
    if not os.path.exists(directory):
        os.makedirs(directory)


def trackDL(trackLink):

	# Figure out mp3 url to save	

	r = requests.get(trackLink, headers=request_header)
	pghtml = r.text
	song_url = re.findall(audioRegex, pghtml)[0]

	# Figure out track title + album from html

	pageContent = requests.get(trackLink)
	tree = html.fromstring(pageContent.content)

	trackTitleID = tree.xpath(titleXpath)
	trackTitleArray = re.findall(titleRegex, trackTitleID[0])
	trackTitleList = list(trackTitleArray[0])
	trackTitle = trackTitleList[1]

	trackAlbumID = tree.xpath(albumXpath)
	trackAlbum = trackAlbumID[0]

	# Find bc user

	bcUserID = re.findall(userRegex, trackLink)
	bcUserList = list(bcUserID[0])
	bcUser = bcUserList[1]

	print(bcUser)
	
	saveTo = directoryPath + bcUser + "\\" + trackAlbum + "\\"

	directoryExists(saveTo)

	with urllib.request.urlopen(song_url) as song_response, open(saveTo + trackTitle + ".mp3", "wb") as out_file:
		shutil.copyfileobj(song_response, out_file)

def albumDL(albumLink):
	# To do.
	print("shit")

def main():

	args = input("Present bandcamp URL:")
	if "/track/" in args:
		trackDL(args)
	elif "/album/" in args:
		albumDL(args)
	else:
		print("nah")

	


if __name__ == "__main__":main()