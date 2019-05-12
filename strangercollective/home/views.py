from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import get_object_or_404, render
from django.contrib  import messages
from .models import *
# Create your views here.

def home(request):
	return render(request, "schome.html")

def temp(request):
	log = []
	titles = ["Absent-Mindedness", "Addiction", "Alcoholism", "Amnesia", "Bad Back", "Bad Grip", "Bad Sight", "Bad Smell", "Bad Temper", "Berserk", "Bestial", "Blindness", "Bloodlust", "Bully", "Callous", "Cannot Learn", "Cannot Speak", "Charitable", "Chronic Depression", "Chronic Pain", "Chummy", "Clueless", "Code of Honor", "Cold-Blooded", "Colorblindness", "Combat Paralysis", "Compulsive Behavior", "Confused", "Cowardice", "Curious", "Cursed", "Deafness", "Debt", "Decreased Time Rate", "Delusions", "Dependency", "Dependents", "Destiny", "Disciplines of Faith", "Disturbing Voice", "Divine Curse", "Draining", "Dread", "Duty", "Dwarfism", "Dyslexia", "Easy to Kill", "Easy to Read", "Electrical", "Enemies", "Epilepsy", "Extra Sleep", "Fanaticism", "Fat", "Fearfulness", "Flashbacks", "Fragile", "Frightens Animals", "G-Intolerance", "Gigantism", "Gluttony", "Greed", "Guilt Complex", "Gullibility", "Ham-Fisted", "Hard of Hearing", "Hemophilia", "Hidebound", "Honesty", "Horizontal", "Hunchback", "Impulsiveness", "Increased Consumption", "Increased Life Support", "Incurious", "Indecisive", "Infectious Attack", "Innumerate", "Insomniac", "Intolerance", "Invertebrate", "Jealousy", "Killjoy", "Kleptomania", "Klutz", "Lame", "Laziness", "Lecherousness", "Lifebane", "Light Sleeper", "Loner", "Low Empathy", "Low Pain Threshold", "Low Self-Image", "Low TL", "Lunacy", "Magic Susceptibility", "Maintenance", "Manic-Depressive", "Megalomania", "Miserliness", "Missing Digit", "Mistaken Identity", "Motion Sickness", "Mundane Background", "Neurological Disorder", "Night Blindness", "Nightmares", "No Depth Perception", "No Fine Manipulators", "No Legs", "No Sense of Humor", "No Sense of Smell/Taste", "Nocturnal", "Noisy", "Non-Iconographic", "Numb", "Oblivious", "Obsession", "Odious Personal Habits", "On the Edge", "One Arm", "One Eye", "One Hand", "Overconfidence", "Overweight", "Pacifism", "Paranoia", "Phantom Voices", "Phobias", "Post-Combat Shakes", "Pyromania", "Quadriplegic", "Reprogrammable", "Restricted Diet", "Restricted Vision", "Revulsion", "Sadism", "Secret", "Secret Identity", "Self-Destruct", "Selfish", "Selfless", "Semi-Upright", "Sense of Duty", "Short Attention Span", "Short Lifespan", "Shyness", "Skinny", "Slave Mentality", "Sleepwalker", "Sleepy", "Slow Eater", "Slow Healing", "Slow Riser", "Social Disease", "Social Stigma", "Space Sickness", "Split Personality", "Squeamish", "Stress Atavism", "Stubbornness", "Stuttering", "Supernatural Features", "Supersensitive", "Susceptible", "Terminally Ill", "Timesickness", "Trademark", "Trickster", "Truthfulness", "Uncontrollable Appetite", "Unfit", "Unhealing", "Unique", "Unluckiness", "Unnatural Features", "Unusual Biochemistry", "Very Fat", "Vow", "Vulnerability", "Weak Bite", "Weakness", "Weirdness Magnet", "Workaholic", "Wounded", "Xenophilia"]
	pages = DisadvantagePage.objects.all()
	for t, p in zip(titles, pages):
		log.append(t)
		log.append("------")
		p.title = t
		p.save()
	# for j in jsob:
	# 	newAd = AdvantagePage.objects.filter(title=j["title"])
	# 	for n in newAd:
	# 		log.append(n.title)
	# 		mtext = j["main"].replace("\n","<br/>")
	# 		mtext = "<p>%s</p>" %(mtext)
	# 		log.append(mtext)
	# 		n.body = mtext
	# 		try:
	# 			text = j["points"].replace("\n","<br/>")
	# 			text = "<p>%s</p>" %(text)
	# 			log.append(text)
	# 			n.points = text
	# 		except: log.append("No Points")
	# 		try:
	# 			text = j["special_limitations"].replace("\n","<br/>")
	# 			text = "<p>%s</p>" %(text)
	# 			log.append(text)
	# 			n.special_limitations = text
	# 		except: log.append("No Limits")
	# 		try:
	# 			text = j["special_enhancements"].replace("\n","<br/>")
	# 			text = "<p>%s</p>" %(text)
	# 			log.append(text)
	# 			n.special_enhancements = text
	# 		except: log.append("No Enhancements")
	# 		n.save()

	return JsonResponse({"log":log})
