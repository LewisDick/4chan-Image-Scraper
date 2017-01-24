import json, urllib, urllib.request, urllib.error, urllib.parse, os, time

location = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))  # Get location of Scrape.py

path = location + "/imgs/"

run = True

if not os.path.exists(path):  # Check if an imgs folder has been made
	os.mkdir(path)

def main():
	start_time = time.time()
	correctURL = False
	url = input("Enter a url (including http://) : ")
	try:
		a, b, c, board, filename, d = url.split("/")
		jsonurl = "http://a.4cdn.org/" + board + "/thread/" + d + ".json"
	except ValueError as e:
		print('Error: Invalid URL')
		return;

	try: #Error handling, avoid program crashing
		req = urllib.request.Request(jsonurl)
		response = urllib.request.urlopen(req)
		data = response.read().decode("utf-8")
		json_data = json.loads(data)['posts']
		correctURL = True
	except ValueError as e: #Invalid Link
		print('Error: Invalid URL')
	except urllib.error.HTTPError as e: #Webpage/site down
		print("It seems like the server is down. Error code : ", e.code)
	except urllib.error.URLError as e: 
		print(e.args)

	noPosts = len(json_data)

	if correctURL:
		for x in range(0, noPosts):
			posts = json_data[x]
			if posts.get("tim") is not None:
				image = urllib.request.urlopen("http://i.4cdn.org/" + board + "/" + str(posts.get("tim")) + posts.get("ext"))
				filename = str(posts.get("tim")) + posts.get("ext")
				file = open(path + filename, "wb")
				file.write(image.read())
				file.close()

		print ("Done. (" + str(round(time.time() - start_time, 2)) + "s)" )

while run:
	main()
	again = input("Repeat with a new link? y or n : ")
	while again.upper() != "Y" and again.upper() != "N":
		again = input("Repeat with a new link? y or n : ")

	if (again.upper() == "N"):
		run = False
	elif (again.upper() == "Y"):
		run = True
