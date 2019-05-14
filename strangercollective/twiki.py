import xmltodict
import json
out = []
with open('wiki.xml') as fd:
	doc = xmltodict.parse(fd.read())
	doc = json.loads(json.dumps(doc))
	doc = doc["mediawiki"]["page"]
	for i in doc:
		try:
			text = i["revision"]["text"]["#text"]
			if "{{Disadvantage Template}}" in text:
				text = text.split("|")
				content = text[7]
				content = content.replace("{{Indent}}Special Limitations","|Special Limitations")
				content = content.replace("{{Indent}}","")
				content = content.replace('<font size="3">',"|")
				scontent = content.split("|")
				apob = {}
				title = i["title"]
				title = title.replace("Disadvantage: ","")

				apob["title"] = title
				apob["main"] = scontent[0]
				pts = text[5]
				pts = pts.replace('<font size="3">',"")
				pts = pts.replace('\'\'',"")
				pts = pts.replace('</font>',"")
				pts = pts.replace('\n',"")
				apob["points"] = pts
				del scontent[0]
				for s in scontent:
					if "Special Limitations\n\n" in s:
						apob["special_limitations"] = s
					if "Special Enhancements\n\n" in s:
						apob["special_enhancements"] = s 
				out.append(apob)
		except: pass

print(json.dumps(out))