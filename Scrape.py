#! /usr/bin/env python3
import json, urllib, urllib.request, urllib.error, urllib.parse, os, time
from queue import Queue
from threading import Thread
import argparse

#TODO
#-----------------------------
#Make the code better
#Add a gui
#Have better error prevention


class DownloadWorker(Thread):
	def __init__(self, queue):
	   Thread.__init__(self)
	   self.queue = queue

	def run(self):
		while True:
			# Get the work from the queue and expand the tuple
			filename, board = self.queue.get()
			download_image(filename, board)
			self.queue.task_done()

# Class made to handle JSON operations. Should allow more extensibility
class JsonWorker():
	def __init__(self, json_data):
		self.json_data=json_data
		self.img_URLS=[]
	
	# Simply returns the list of file URLs. Most code taken from pull_image_urls function
	def getImageURLs(self):
		noPosts = len(self.json_data)
		for x in range(0, noPosts):
			posts = self.json_data[x]
			if posts.get("tim") is not None:
				currentImgURL = str(posts.get("tim")) + posts.get("ext")
				self.img_URLS.append(currentImgURL)
		print(str(len(self.img_URLS)) + " Images Found")
		return self.img_URLS

	# Returns the filepath string to the directory to store the files.
	#TODO --- Move creating the directory to its own class function
	def getPath(self):
		location=os.path.realpath(os.getcwd())
		global folder_increment
		#location = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
		if not args.d:
			path = location + "/imgs/"
		else:
			# Prioritizing the thread subject, then part of the comment
			if self.json_data[0].get('sub') is not None:
				path=location+"/"+self.json_data[0].get('sub')+"/"
			elif self.json_data[0].get('com') is not None:
				try:
					path=location+'/'+self.json_data[0].get('com')[:49]+'/'
				except:
					path=location+'/imgs'+str(folder_increment)+'/'
					folder_increment+=1
		try:
			if not os.path.exists(path):  
				os.mkdir(path)
		except FileNotFoundError as e: #should prevent issues with illegal filename characters + length
			path=location+'/imgs'+str(folder_increment)+'/'
			folder_increment+=1
			if not os.path.exists(path):  
				os.mkdir(path)
		return path

img_URLS = []
folder_increment=0
path=''
invalid_link = True
run = True

def main():

	if args.url is not None:
		url=args.url
		print(args.url)
	else:
		url = input("Enter a url (including http://) : ")
	url_parts = handle_url(url)
	invalid_link = False
	pull_image_urls(url_parts[0], url_parts[1])

	queue = Queue()
   # Create 8 worker threads
	for x in range(10):
		worker = DownloadWorker(queue)
		# Setting daemon to True will let the main thread exit even though the workers are blocking
		worker.daemon = True
		worker.start()
	global img_URLS
	for file in img_URLS:
		queue.put((file, url_parts[1]))

	queue.join()

def handle_url(input):
	#Add handling of links without http, https and with json at the end maybe?
	try:
		http, slash, slash1, board, thread, threadNo = input.split("/")
		json_url = "http://a.4cdn.org/" + board + "/thread/" + threadNo + ".json"
		invalid_link = False
	except ValueError as e:
		print('Error: Invalid URL')
		return; #Exit current

	return [json_url, board]

def pull_image_urls(url, board):

	try: #Error handling, avoid program crashing
		req = urllib.request.Request(url)
		response = urllib.request.urlopen(req)
		data = response.read().decode("utf-8")
		json_data = json.loads(data)['posts']
	except ValueError as e: #Invalid Link
		print('Error: Invalid URL')
		return
	except urllib.error.HTTPError as e: #Webpage/site down
		print("It seems like the server is down. Error code : ", e.code)
		return
	except urllib.error.URLError as e:  #Any other error
		print(e.args)
		return

	JSON=JsonWorker(json_data)
	global img_URLS
	img_URLS=JSON.getImageURLs()
	global path
	path=JSON.getPath()

def download_image(img_URL, board):
	image = urllib.request.urlopen("http://i.4cdn.org/" + board + "/" + img_URL)
	file = open(path + img_URL, "wb")
	file.write(image.read())



# Defining command line arguments
parser=argparse.ArgumentParser()
parser.add_argument('url', help='URL to grab images from. Will be asked for if not supplied', nargs='?')
parser.add_argument('-n', help='Program will exit rather than ask for additional URLs', action='store_true')
parser.add_argument('-d', help='Images will be saved in folders specific to each thread', action='store_true')
# Prioritize thread subject then beginning of comment
args=parser.parse_args()

while run: #Loops while the user wants to keep going
	main()
	# Resets the url argument to none so that it doesn't run the same url again
	args.url=None
	if not args.n:
		again = input("Repeat with a new link? y or n : ")
	else:
		again = 'N'
	while again.upper() != "Y" and again.upper() != "N":
		again = input("Repeat with a new link? y or n : ")

	if (again.upper() == "N"):
		run = False
	elif (again.upper() == "Y"):
		run = True





