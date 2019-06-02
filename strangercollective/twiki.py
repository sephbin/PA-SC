import xmltodict
import json
import re



out = []
with open('wiki.xml') as fd:
	doc = xmltodict.parse(fd.read())
	doc = json.loads(json.dumps(doc))
	doc = doc["mediawiki"]["page"]
	for i in doc:
		try:
			text = i["revision"]["text"]["#text"]
			if "{{Modifier Template}}" in text:
				# text = text.split("|")
				content = text
				content = content.replace("\n\n","|")
				content = content.replace("{{Indent}}Special Limitations","|Special Limitations")
				content = content.replace(">Defaults:",">|Defaults:")
				content = content.replace("</font>","|</font>")
				content = content.replace(">Prerequisites:",">|Prerequisites:")
				content = content.replace("<i>Modifiers:","<i>|Modifiers:")
				content = content.replace("{{Indent}}","")
				content = content.replace('<font size="3">',"|")
				content = content.replace("</i>","|</i>")
				scontent = content.split("|")
				# print(scontent)
				sco = []
				for s in scontent:
					a = "<" not in s
					b = "{" not in s
					c = '="' not in s
					if a and b and c:
						sco.append(s)
				scontent = sco
				apob = {}
				title = i["title"]
				title = title.replace("Skill: ","")
				title = title.replace("Modifier: ","")

				apob["title"] = title
				other = []
				for t in scontent:
					if re.search("^''", t):
						t = t.replace("''", "")
						apob["modifier"] = t
				# 	elif re.search("^Prerequisite", t):
				# 		t = t.replace("Prerequisites: ", "")
				# 		t = t.replace("Prerequisites:", "")
				# 		t = t.replace("Prerequisite: ", "")
				# 		apob["prerequisites"] = t
				# 	elif re.search("^''", t):
				# 		t = t.replace("''", "")
				# 		t = t.split("/")
				# 		apob["attribute"] = t[0]
				# 		apob["challenge"] = t[1]
					else:
						other.append(t)
				other = sorted(other, key=len)
				apob["body"] = other[-1]


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
				out.append(apob)
		except: pass

print(json.dumps(out))