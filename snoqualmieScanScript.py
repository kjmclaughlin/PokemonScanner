#!/usr/bin/python
import requests, json, random, sys, smtplib, time

from email.mime.text import MIMEText

def generateEmailList(emailFile):
    emailFile = open(emailFile, "r")
    emails = emailFile.readlines()
    output = []
    for email in emails:
        output.append(email.strip())
    return output

topLeftLat = 47.54484384921419
topLeftLong = -121.8889331817627
bottomRightLat = 47.52531550240097
bottomRightLong = -121.84807777404787

path = "/PokemonGO/"

pokemonIds = []
pokemonFound = {}
idToPokemonDictionary = {} #This dictionary keys from id number to name for converting input lists
pokemonToIdDictionary = {} #This dictionary keys from name to id number for converting input lists
emailList = generateEmailList(path + "SnoqualmieEmailList.txt")
fromAddress = "PokemonGoEmailer@gmail.com"
messageBody = ""
pokemonFile = open(path + "pokemonList.txt", "r")
desiredPokemonFile = open(path + "desiredPokemon.txt", "r")
desiredPokemonList = desiredPokemonFile.readlines()
fullPokemonList = pokemonFile.readlines()
for i in range(0, (len(fullPokemonList))):
        pokemonToIdDictionary[fullPokemonList[i].strip()] = i + 1
        idToPokemonDictionary[i + 1] = fullPokemonList[i].strip()
for pk in desiredPokemonList:
	pokemonIds.append(pokemonToIdDictionary[pk.strip()])

def main():
	log = open("/Logs/SnoqualmiePokemonLogs", "a");
	sys.stdout = log;
	x = topLeftLong
	step = 1.0 / 10.0 #Num scans to cover x and y, total scans is denom^2
	dx = (bottomRightLong - topLeftLong) * step
	dy = (bottomRightLat - topLeftLat) * step
	while x < bottomRightLong:
		y = topLeftLat
		while y > bottomRightLat:
			url = "https://pokevision.com/map/data/"
			url += str(y) + '/' + str(x)
			r = requests.get(url)
			c = json.loads(r.content)
			for p in c['pokemon']:
				if p['pokemonId'] in pokemonIds:
					lat = str(p['latitude'])
					lon = str(p['longitude'])
					if (pokemonFound.has_key(p['pokemonId']) == False):
						pokemonFound[p['pokemonId']] = p
					else:
						pokemonFound[p['pokemonId']] = p
			y += dy
		x += dx
	print("\n\n\n")
	print("Pokemon Found:\n")
	print(pokemonFound)
        messageBody = ""
        for k in pokemonFound.keys():
                messageBody += str(idToPokemonDictionary[pokemonFound[k]['pokemonId']]) + \
                               " found at coordinates: http://maps.google.com/maps?q=" + \
                                str(pokemonFound[k]['latitude']) + "," + \
                                str(pokemonFound[k]['longitude']) + "\n\t" + \
                                "Expires at: " + \
                                time.strftime("%I:%M%p and %S seconds", time.localtime(pokemonFound[k]['expiration_time'] - (60 * 60 * 7))) + \
                                "\n"
        print messageBody
        password = open(path + "GmailLogin.txt", "r").readlines()[0].strip()
        smtpStr = 'smtp.gmail.com'
        smtpPort = 587
        if messageBody is not "":
                msg = MIMEText(messageBody)
                msg['Subject'] = "PokemonGo Rare Pokemon Update"
                msg['From'] = fromAddress
                smtp_serv = smtplib.SMTP(smtpStr, smtpPort)
                smtp_serv.ehlo_or_helo_if_needed()
                smtp_serv.starttls()
                smtp_serv.ehlo()
                smtp_serv.login(fromAddress, password)
                for addr in emailList:
                        msg['To'] = addr
                        smtp_serv.sendmail(fromAddress, addr, msg.as_string())
                smtp_serv.quit()

main()
