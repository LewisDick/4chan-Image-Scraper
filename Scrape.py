import urllib, urllib.request, urllib.error, urllib.parse, os
from bs4 import BeautifulSoup

user_agent = 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.0.7) Gecko/2009021910 Firefox/3.0.7'
headers = {'User-Agent':user_agent,} #Headers needed to allow website access

location = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__))) #Get location of Scrape.py

path = location + "/imgs/"

if not os.path.exists(path): #Check if an imgs folder has been made
	os.mkdir(path)

def getImages():
	count = 0
	correctURL = False
	url = input("Enter a url (including http://) : ")
<<<<<<< HEAD
	try:
		a, b, c, board, filename, d = url.split("/")
		jsonurl = "http://a.4cdn.org/" + board + "/thread/" + d + ".json"
	except ValueError as e:
		print('Error: Invalid URL')
		invalidValue = True
=======
>>>>>>> parent of 1ea54cc... Complete rewrite, uses the 4chan api instead of BeautifulSoup.

	try: #Error handling, avoid program crashing
		req = urllib.request.Request(url,None, headers)
		response = urllib.request.urlopen(req)
		data = response.read().decode("utf-8")
		correctURL = True
	except ValueError as e: #Invalid Link
		print('Error: Invalid URL')
	except urllib.error.HTTPError as e: #Webpage/site down
		print("It seems like the server is down. Error code : ", e.code)
	except urllib.error.URLError as e: 
		print(e.args)

	if correctURL:
		soup = BeautifulSoup(data, 'html.parser')
		imgs = soup.findAll("a", attrs={"class": "fileThumb", "href":True}) #Search data for image links
		num = len(imgs) #Number of files being downloaded

		for a in imgs:
			count += 1
			print(str(count) +"/"+str(num)) #Gives indication of progress
			img_url = a["href"]
			img_data = urllib.request.urlopen("http:" + img_url)
			a,b,c,d,filename = img_url.split("/") #Seperate filename from rest of href
			file = open(path+filename, "wb")
			file.write(img_data.read())
			file.close()

		print("Done")

	again = input("Repeat with a new link? y or n : ")
	while again.upper() != "Y" and again.upper() != "N":
		again = input("Repeat with a new link? y or n : ")
	
	if(again.upper() == "Y"):
		getImages(); #Repeat
	elif(again.upper() == "N"):
		print("Finished.")
		
getImages();#Run