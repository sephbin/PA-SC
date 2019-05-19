import xmltodict
import json
titlelist = ["Appendix Test", "Asbjorn", "Asbjørn", "Asherin Cosmology", "Axel Svärdstein", "Britvah", "Bull Ant", "Campaign Notes", "Charlie Moody", "Cleştarterra", "Daly", "Eidolon 1", "Emmett Blakely", "Eorith Magic", "Fell Deer", "Gurps Conversion", "Gurps Occupational Templates", "Gutz", "Gútz", "Iron Downs", "Kavenderblight", "Lindon", "Main Page", "Moody Island", "Nick", "Niko Zabanias", "Nodes", "Oceanic Magic", "Ramsbeard", "Resources: Image Links", "Sirquine Plains", "Svell Dwarves", "Test", "Test Test Test Test", "The Ivory Triangle", "Wasp Swarm", "Whop Wha Waa", "Widget:Google Spreadsheet", "Wolf Spider"]
out = []
with open('wiki.xml') as fd:
	doc = xmltodict.parse(fd.read())
	doc = json.loads(json.dumps(doc))
	doc = doc["mediawiki"]["page"]
	for i in doc:
		if i["title"] in titlelist:
			print("###",i["title"])
			print(i["revision"]["text"]["#text"])
			print("---------------------------------------------------------------------------------")
			print("\n\n\n\n\n\n\n\n\n\n")
		# try:
		# 	text = i["revision"]["text"]["#text"]
		# 	if "{{Disadvantage Template}}" in text:
		# 		text = text.split("|")
		# 		content = text[7]
		# 		content = content.replace("{{Indent}}Special Limitations","|Special Limitations")
		# 		content = content.replace("{{Indent}}","")
		# 		content = content.replace('<font size="3">',"|")
		# 		scontent = content.split("|")
		# 		apob = {}
		# 		title = i["title"]
		# 		title = title.replace("Disadvantage: ","")

		# 		apob["title"] = title
		# 		apob["main"] = scontent[0]
		# 		pts = text[5]
		# 		pts = pts.replace('<font size="3">',"")
		# 		pts = pts.replace('\'\'',"")
		# 		pts = pts.replace('</font>',"")
		# 		pts = pts.replace('\n',"")
		# 		apob["points"] = pts
		# 		del scontent[0]
		# 		for s in scontent:
		# 			if "Special Limitations\n\n" in s:
		# 				apob["special_limitations"] = s
		# 			if "Special Enhancements\n\n" in s:
		# 				apob["special_enhancements"] = s 
		# 		out.append(apob)
		# except: pass

print(json.dumps(out))