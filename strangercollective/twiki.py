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
			if "{{Advantage Template}}" in text:
				text = text.split("|")
				content = text[7]
				content = content.replace("{{Indent}}","")
				content = content.replace('<font size="3">',"|")
				scontent = content.split("|")
				apob = {}
				apob["title"] = i["title"]
				apob["main"] = scontent[0]
				del scontent[0]
				for s in scontent:
					if "'Special Limitations'" in s:
						apob["special_limitations"] = s
					if "'Special Enhancements'" in s:
						apob["special_enhancements"] = s 
				out.append(apob)
		except: pass

print(json.dumps(out))