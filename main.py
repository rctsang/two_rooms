import os
import email, smtplib, ssl, csv
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage

import random as rand
from datetime import datetime as dt

#################################
########### Get Emails ##########
#################################

with open('contact.csv') as f:
	reader = csv.reader(f)
	data = list(reader)

# print(data)  <-- "data" is the name of the list of lists [[Name, Email],..]

addresses = [d[1] for d in data]
num_players = len(addresses)

#################################
########### Card Class ##########
#################################

class Card:

	img_dir = "images/"

	def __init__(self, team, role=""):
		self.team = team
		self.role = role

	# Function to get the name of the card's graphic
	# Note: The card's role must not be normal
	
	# Params: 	None
	# Out:		(String)	Image filename
	def getImage(self):
		if not self.role:
			return self.img_dir + self.team + ".jpg"
		return self.img_dir + self.role + ".jpg"

	# Function to get the card's team

	# Params:		None
	# Out:		(String)	Team color
	def getTeam(self):
		return self.team

	# Function to get the Card role
	# Note: Only use this for the purposes of printing the role

	# Params:		None
	# Out:		(String)	Player Role
	def getRole(self):
		if not self.role:
			return "Player"
		return self.role



########################################
####### Construct/Shuffle Deck #########
########################################

if (num_players < 4):
	print("Error: Not Enough Players!")
	exit()

deck = [Card("Blue", "President"), Card("Red", "Bomber")]

for n in range(0, (num_players - 2) // 2):
	deck += [Card("Red")]
	deck += [Card("Blue")]

if (num_players % 2):
	deck += [Card("Grey", "Gambler")]


rand.seed()

shuffled_deck = rand.sample(deck, len(deck))

directory = dict(zip(addresses, shuffled_deck))

# debugging
for k in directory.keys():
	print(k, directory[k].getImage())



#################################
########## Send Emails ##########
#################################

port = 465  # For SSL
smtp_server = "smtp.gmail.com"

# Replace message with a .txt for non-coders to use

timestamp = str(dt.now())[:16]

subject = "Two Rooms Test: " + timestamp

sender_email = "tworoomskoinberk@gmail.com"  # Enter your address
password = input("Type your password and press enter: ")

filepath = ""

if input("Ready to send? (y/n) ") == "n":
	exit()

context = ssl.create_default_context()
with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
    server.login(sender_email, password)

    for person in data:

    	# Create Multipart Section and Header
    	message = MIMEMultipart()
    	message["From"] = sender_email
    	message["Subject"] = subject

    	player_card = directory[person[1]]
    	message["To"] = person[1]

    	# get image filename
    	filepath = player_card.getImage()

    	# debugging
    	print(message["To"], filepath)

    	with open(filepath, 'rb') as img:
    		img_data = img.read()

    	# Write Custom Body w/ Name, Team, Role

    	greetings = "Hi " + str(person[0]) + ",\n\n"
    	info1 = "You are on the " + player_card.getTeam() + " team.\n\n"
    	info2 = "Your role is: " + player_card.getRole()
    	body = greetings + info1 + info2

    	text = MIMEText(body) # TODO: Customize this
    	message.attach(text)

    	image = MIMEImage(img_data, name=os.path.basename(filepath))
    	message.attach(image)

    	server.sendmail(message["From"], message["To"], message.as_string())











