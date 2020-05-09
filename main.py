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
	def getImage(self, for_link=False):
		if for_link:
			if not self.role:
				return self.team + ".jpg"
			return self.role + ".jpg"

		if not self.role:
			return self.img_dir + self.team + ".jpg"
		return self.img_dir + self.role + ".jpg"

	# Function to get the card's team

	# Params:		None
	# Out:		(String)	Team color
	def getTeam(self):
		return self.team

	
	# Function to get the Card role
	# Note: Will need to adjust HERE if adding additional roles

	# Params:		None
	# Out:		(String)	Player Role
	def getRole(self):
		if not self.role:
			return "Player"
		if self.role == "MayorBlue":
			return "Blue Mayor"
		if self.role == "MayorRed":
			return "Red Mayor"
		if self.role == "SpyBlue":
			return "Blue Spy"
		if self.role == "SpyRed":
			return "Red Spy"
		return self.role



########################################
####### Construct/Shuffle Deck #########
########################################

if (num_players < 2):
	print("Error: Not Enough Players!")
	exit()

deck = [Card("Blue", "President"), Card("Red", "Bomber")]

special = 2

if (special+2 < num_players) and (input("Play with the Doctor/Engineer? (y/n) ") == "y"):
	deck += [Card("Blue", "Doctor")]
	deck += [Card("Red", "Engineer")]
	special += 2

if (special+2 < num_players) and (input("Play with the Mayors? (y/n) ") == "y"):
	deck += [Card("Blue", "MayorBlue")]
	deck += [Card("Red", "MayorRed")]
	special += 2

if (special+2 < num_players) and (input("Play with the Spies? (y/n) ") == "y"):
	deck += [Card("Blue", "SpyBlue")]
	deck += [Card("Red", "SpyRed")]
	special += 2

for n in range(0, (num_players - special) // 2):
	deck += [Card("Red")]
	deck += [Card("Blue")]

if (num_players % 2):
	deck += [Card("Grey", "Gambler")]


rand.seed()

shuffled_deck = rand.sample(deck, len(deck))

directory = dict(zip(addresses, shuffled_deck))   # directory contains dictonary w/ key=email, value=Card object

# debugging
# for k in directory.keys():
# 	print(k, directory[k].getImage(), directory[k].getRole())



#################################
########## Send Emails ##########
#################################

port = 465  # For SSL
smtp_server = "smtp.gmail.com"

# Replace message with a .txt for non-coders to use

timestamp = str(dt.now())[:16]

subject = "Two Rooms Test: " + timestamp

###################### USER EDITED ##############################

sender_email = "koinberk2rooms@gmail.com"  # TODO: Enter your address

#################################################################

if input("Deck has been shuffled and dealt.\nReady to send? (y/n) ") == "n":
	exit()

password = input("Type your password and press enter: ")

filepath = ""
body = "{n},\nTeam: {t}\nRole: {r}\nImg: {l}"

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

    	# # debugging
    	# print(message["To"], filepath)

    	with open(filepath, 'rb') as img:
    		img_data = img.read()

    	# Write Custom Body w/ Name, Team, Role, Url to Images

    	# greetings = "Hi " + str(person[0]) + ",\n\n"
    	# info1 = player_card.getTeam() + " team.\n\n"
    	# info2 = "Role: " + player_card.getRole() + "\n\n"
    	# info3 = "View card here: \n"
    	# link = "https://tinyurl.com/2r-cards/" + str(player_card.getImage())

    	body = body.format(n=person[0], 
    						t=player_card.getTeam(), 
    						r=player_card.getRole(),
    						l="https://tinyurl.com/2r-cards/" + player_card.getImage(for_link=True))

    	# adding body and image attachment to email

    	text = MIMEText(body)
    	message.attach(text)

    	image = MIMEImage(img_data, name=os.path.basename(filepath))
    	message.attach(image)

    	# Sending email
    	print("Sending email to:", message["To"], "...")
    	server.sendmail(message["From"], message["To"], message.as_string())











