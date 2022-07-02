from django.contrib  import messages
from django.contrib.auth.models import User
from django.db import transaction
from django.forms.models import model_to_dict
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.urls import reverse
from django.shortcuts import get_object_or_404, render, redirect
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required, user_passes_test

import sys, os
from django.conf import settings
from django.contrib.auth.models import User, Group
from django.db.models import Q
from django.shortcuts import get_object_or_404, render, redirect
from .models import *
# import ghhops_server as hs
import rhino3dm

def getPayload(request):
	import json
	d = {}
	try:
		d = json.loads(str(request.body, encoding='utf-8'))
	except Exception as e:
		print(e)
		if request.method == "GET":
			try:	d = dict(request.GET)
			except: pass
		if request.method == "POST":
			try:	d = dict(request.POST)
			except: d = json.loads(str(request.body, encoding='utf-8'))
		if request.method == "DELETE":
			try:	d = json.loads(str(request.body, encoding='utf-8'))
			except: pass
	return d

def errorLog(e, log=[]):
	exc_type, exc_obj, exc_tb = sys.exc_info()
	other = sys.exc_info()[0].__name__
	fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
	errorType = str(exc_type)
	errob = {"isError": True, "error":str(e), "errorType":errorType, "function":fname, "line":exc_tb.tb_lineno, "log":log}
	return errob

def getSecure():
	try:
		file = open("C:\\secure\\secure.json",
			"r")
		out = file.read()
		file.close()
		return json.loads(out)
	except Exception as e:
		#dblog(e)
		return {}

def isUser(request):
	user = None
	try:	sqlcheck(request, getSecure()["dtvsn"]["username"], getSecure()["dtvsn"]["password"])
	except: pass
	try:
		bearer = request.META["HTTP_AUTHORIZATION"].replace("Bearer ","")
		dblog(bearer)
		try:
			dblog("try")
			srequ = get_object_or_404(samlrequest, nonce = bearer)
			dblog("Try worked")
			dblog(srequ)
		except Exception as e:
			dblog("except")
			dblog(e)
			srequ = get_object_or_404(standardrequest, nonce = bearer)
			dblog("Except worked")
			dblog(srequ)
		user = srequ.user
	except:
		if request.user.is_authenticated:
			user = request.user
	return user
def from_json(json_obj):
	"""Convert to rhino3dm from json"""
	return rhino3dm.CommonObject.Decode(json_obj)

def _coerce_value(param_type, param_data):
	import rhino3dm
	import json
	# get data as dict
	
	# parse data
	# print(param_type)
	if param_type.startswith("Rhino.Geometry.Point3d"):
		data = json.loads(param_data)
		data = {k.lower(): v for k, v in data.items()}
		return rhino3dm.Point3d(**data)
	if param_type.startswith("Rhino.Geometry."):
		data = json.loads(param_data)
		return from_json(data)
	if param_type.startswith("System.String"):
		data = eval(param_data)
		try: data = json.loads(data)
		except Exception as e: print(e)
		return data
	if param_type.startswith("System.Double"):
		data = float(param_data)
		return data
	return param_data

def parse_params(payload):
	outOb = {"payload":payload}
	for hopsInput in payload["values"]:
		# print(hopsInput)
		upOb = []
		for treeAdress, treeBranch in hopsInput["InnerTree"].items():
			apOb = []
			outOb[hopsInput["ParamName"]+"_original"] = treeBranch
			for hopsObject in treeBranch:
				try:
					a = _coerce_value(hopsObject["type"],hopsObject["data"])
					apOb.append(a)
					# print("-"*4,a)
				except Exception as e:
					apOb.append(None)
					# print(errorLog(e))
					pass
			upOb.append(apOb)
		if len(upOb) < 2:
			upOb = upOb[0]
		outOb[hopsInput["ParamName"]] = upOb
	return outOb
@csrf_exempt
def getRequest(request):
	pass
	# structure = {
	# 		"Python": {"version":str(sys.version), "info":str(sys.version_info)},
	# 		"Description": "run GET request",
	# 		"Inputs": [
	# 			# {"Name": "url", "Nickname": "url", "Description": "url", "ParamType": "Text", "ResultType": "System.String", "Default":None, "AtLeast": 1, "AtMost": 2147483647},
	# 			{"Name": "url", "Nickname": "url", "Description": "url", "ParamType": "Text", "ResultType": "System.String", "Default":None, "AtLeast": 1, "AtMost": 1},
	# 			{"Name": "headers", "Nickname": "head", "Description": "headers", "ParamType": "Text", "ResultType": "System.String", "Default":None, "AtLeast": 1, "AtMost": 1},
	# 		],
	# 		"Outputs": [{"Name": "Log", "Nickname": "L", "Description": "Log", "ParamType": "Text", "ResultType": "System.String", "AtLeast": 1, "AtMost": 1},
	# 			{"Name": "Output", "Nickname": "O", "Description": "Output", "ParamType": "Text", "ResultType": "System.String", "AtLeast": 1, "AtMost": 1},
	# 		]}
	# if request.method =="GET":
	# 	return JsonResponse(structure)

	# elif request.method =="POST":
	# 	import requests
	# 	log = []
	# 	payload = parse_params(getPayload(request))
	# 	# print(payload)
	# 	outOb = {"type": "System.String", "data": "\"\""}

	# 	out = {"values": [
	# 		{"ParamName": "Log", "InnerTree": {"0": str(log), }},
	# 		{"ParamName": "Output", "InnerTree": {"0": outOb, }},
	# 	]}
	# 	# print(out)
	# 	return JsonResponse(out)

	# else:
	# 	print("?")
	# 	return JsonResponse({"error":True})

@csrf_exempt
def solve(request):
	if request.method =="GET":
		return JsonResponse({})

	elif request.method =="POST":
		payload = parse_params(getPayload(request))
		function = payload["payload"]["pointer"]
		if function.endswith("/"):
			function = function.split("/")[-2]
		else:
			function = function.split("/")[-1]
		function = globals()[function]
		out = function(request, payload)
		return JsonResponse(out)

def packMono(request, payload={}):
	import time
	log=[]
	start_time = time.time()
	name = "packMono"
	structure = {
		"Python": {"version":str(sys.version), "info":str(sys.version_info)}, "Category": "Hops", "Subcategory": "Hops Python", "Uri": "/"+name, "Name": name, "Nickname": name, "Description": name,
		"Inputs": [
			# {"Name": "url", "Nickname": "url", "Description": "url", "ParamType": "Text", "ResultType": "System.String", "Default":None, "AtLeast": 1, "AtMost": 2147483647},
			{"Name": "majorGraph", "Nickname": "M", "Description": "majorGraph", "ParamType": "Text", "ResultType": "System.String", "Default":None, "AtLeast": 1, "AtMost": 1},
			{"Name": "subGraphs", "Nickname": "S", "Description": "subGraphs", "ParamType": "Text", "ResultType": "System.String", "Default":None, "AtLeast": 1, "AtMost": 2147483647},
		],
		"Outputs": [{"Name": "Log", "Nickname": "L", "Description": "Log", "ParamType": "Text", "ResultType": "System.String", "AtLeast": 1, "AtMost": 1},
			{"Name": "Output", "Nickname": "O", "Description": "Output", "ParamType": "Text", "ResultType": "System.String", "AtLeast": 1, "AtMost": 1},
		]}
	if request.method =="GET":	return JsonResponse(structure)
	if payload != {}:
		import networkx as nx
		from networkx.algorithms import isomorphism
		import json
		majorGraph = payload["majorGraph"]
		graph = majorGraph[0]

		# graph = [{"_connected":[1, 6],"type":"a"}, {"_connected":[0, 2, 11],"type":"a"}, {"_connected":[1, 3, 12],"type":"a"}, {"_connected":[2, 4, 13],"type":"a"}, {"_connected":[3, 5, 14],"type":"a"}, {"_connected":[4, 15],"type":"a"}, {"_connected":[0, 7, 11],"type":"a"}, {"_connected":[6, 8, 16],"type":"a"}, {"_connected":[7, 9, 17],"type":"a"}, {"_connected":[8, 10, 18],"type":"a"}, {"_connected":[9, 19],"type":"a"}, {"_connected":[6, 12, 1, 16],"type":"a"}, {"_connected":[11, 13, 2, 20],"type":"a"}, {"_connected":[12, 14, 3, 21],"type":"a"}, {"_connected":[13, 15, 4, 22],"type":"a"}, {"_connected":[14, 5, 23],"type":"a"}, {"_connected":[11, 17, 7, 20],"type":"a"}, {"_connected":[16, 18, 8, 24],"type":"a"}, {"_connected":[17, 19, 9, 25],"type":"a"}, {"_connected":[18, 10, 26],"type":"a"}, {"_connected":[16, 21, 12, 24],"type":"a"}, {"_connected":[20, 22, 13, 27],"type":"a"}, {"_connected":[21, 23, 14, 28],"type":"a"}, {"_connected":[22, 15, 29],"type":"a"}, {"_connected":[20, 25, 17, 27],"type":"a"}, {"_connected":[24, 26, 18, 30],"type":"a"}, {"_connected":[25, 19, 31],"type":"a"}, {"_connected":[24, 28, 21, 30],"type":"a"}, {"_connected":[27, 29, 22, 32],"type":"a"}, {"_connected":[28, 23, 33],"type":"a"}, {"_connected":[27, 31, 25, 32],"type":"a"}, {"_connected":[30, 26, 34],"type":"a"}, {"_connected":[30, 33, 28, 34],"type":"a"}, {"_connected":[32, 29, 35],"type":"a"}, {"_connected":[32, 31, 35],"type":"a"}, {"_connected":[34, 33],"type":"a"}]
		# sub_graph = [{"_connected": [1, 4], "type": "a"},{"_connected": [0, 5], "type": "a"},{"_connected": [3, 4], "type": "a"},{"_connected": [2, 7], "type": "a"},{"_connected": [2, 5, 0, 7], "type": "a"},{"_connected": [4, 6, 1, 9], "type": "a"},{"_connected": [5, 10], "type": "a"},{"_connected": [4, 8, 3, 9], "type": "a"},{"_connected": [7, 11], "type": "a"},{"_connected": [7, 10, 5, 11], "type": "a"},{"_connected": [9, 6], "type": "a"},{"_connected": [9, 8], "type": "a"}]
		sub_graphs = list(map(lambda x: get_object_or_404(graphObject, name=x).data, payload["subGraphs"]))
		# print(sub_graphs)
		# sub_graphs = [
		# [{"_connected": [1, 3], "type": "a"},{"_connected": [0, 2, 5], "type": "a"},{"_connected": [1, 6], "type": "a"},{"_connected": [0, 4, 5], "type": "a"},{"_connected": [3, 7], "type": "a"},{"_connected": [3, 6, 1, 7], "type": "a"},{"_connected": [5, 2, 8], "type": "a"},{"_connected": [5, 4, 8], "type": "a"},{"_connected": [7, 6], "type": "a"}],
		# [{"_connected": [1, 2], "type": "a"},{"_connected": [0, 3], "type": "a"},{"_connected": [0, 3], "type": "a"},{"_connected": [2, 1], "type": "a"}],
		# [{"_connected": [1, 2], "type": "a"},{"_connected": [0, 5], "type": "a"},{"_connected": [0, 3, 5], "type": "a"},{"_connected": [2, 4, 6], "type": "a"},{"_connected": [3, 7], "type": "a"},{"_connected": [2, 1, 6], "type": "a"},{"_connected": [5, 7, 3], "type": "a"},{"_connected": [6, 4], "type": "a"}],
		# [{"_connected": [1, 3], "type": "a"},{"_connected": [0, 2, 6], "type": "a"},{"_connected": [1, 7], "type": "a"},{"_connected": [0, 4, 6], "type": "a"},{"_connected": [3, 5, 8], "type": "a"},{"_connected": [4, 9], "type": "a"},{"_connected": [3, 7, 1, 8], "type": "a"},{"_connected": [6, 2, 10], "type": "a"},{"_connected": [6, 9, 4, 10], "type": "a"},{"_connected": [8, 5, 11], "type": "a"},{"_connected": [8, 7, 11], "type": "a"},{"_connected": [10, 9], "type": "a"}],
		# ]

		graphNodes = []
		graphEdges = []

		for index, node in enumerate(graph):
			delList = []
			# print(index, node, type(node))
			for k in node:
				if k.startswith("_"):
					delList.append(k)
			for k in delList:
				if k == "_connected":
					for target in node[k]:
						graphEdges.append((index,target))
				del node[k]
			node["index"] = index
			apob = (index, node)
			graphNodes.append(apob)
		G = nx.Graph()
		G.add_nodes_from(graphNodes)
		G.add_edges_from(graphEdges)

		def sub_graph_function(primary_graph, sub_graphs, used_index=[], nest=[]):
			n = "".join(nest)
			for sub_graph_index, sub_graph in enumerate(sub_graphs):
				if sub_graph_index in used_index:
					continue
				# print(n,sub_graph_index,"-"*100)
				# print(n,sub_graph_index,used_index, sub_graph)
				sub_graphNodes = []
				sub_graphEdges = []

				for index, node in enumerate(sub_graph):
					delList = []
					for k in node:
						if k.startswith("_"):
							delList.append(k)
					for k in delList:
						if k == "_connected":
							for target in node[k]:
								sub_graphEdges.append((index,target))
						del node[k]
					#print(n,index,node)       
					apob = (index, node)
					sub_graphNodes.append(apob)
				#print(n,sub_graphNodes)
				SG = nx.Graph()
				SG.add_nodes_from(sub_graphNodes)
				SG.add_edges_from(sub_graphEdges)
				#print(n,"SG",SG)

				GM = isomorphism.GraphMatcher(primary_graph, SG)
				SGM = GM.subgraph_isomorphisms_iter()
				log.append(time.time() - start_time)
				layout_options = []
				# print(n,sub_graph_index, "length", len(list(SGM)))
				for result_index, result in enumerate(SGM):
					# layout_options.append(result)
					resultIsGood = True
					for k,v in result.items():
						SGNode = SG.nodes[int(v)]
						GNode = primary_graph.nodes[int(k)]
						if SGNode["type"] not in GNode["type"]:
							# layout_options.remove(result)
							resultIsGood = False
					# print(n,sub_graph_index,".",result_index, resultIsGood)
					if resultIsGood:
						layout_options.append(result)
						# print(n,sub_graph_index,primary_graph)
						graph_clone = primary_graph.copy()
						used_nodes = list(result.keys())
						used_nodes.reverse()
						# print(n,sub_graph_index, used_nodes)
						for node in used_nodes:
							graph_clone.remove_node(node)
						# print(n,sub_graph_index,"running r_i_g", used_index+[sub_graph_index])
						# print(n,sub_graph_index,"lo1",layout_options)
						suboptions = sub_graph_function(graph_clone, sub_graphs, used_index+[sub_graph_index], nest+["\t"])
						if suboptions:
							# print(n,sub_graph_index,".",result_index,json.dumps(result),json.dumps(suboptions))
							layout_options = layout_options+suboptions
							break
						else:
							break
					# if result_index > 1:
						# break
					# print(n,sub_graph_index,".",result_index)
				# print(n,sub_graph_index,"^"*100)
				return layout_options

					# print("results -->",result, resultIsGood)

		out = sub_graph_function(G, sub_graphs)
		# print(json.dumps(out))
			# 	print("results -->",result, resultIsGood)
			# print("options", , json.dumps(layout_options))

		outputContent = json.dumps(out)
		log.append("--- %s seconds ---" % (time.time() - start_time))
		log = json.dumps(list(map(lambda x: str(x), log)))
		out = {"values": [
			{"ParamName": "Log", "InnerTree": {"0": [{"type": "System.String", "data": "\""+log+"\""}]}},
			{"ParamName": "Output", "InnerTree": {"0": [{"type": "System.String", "data": "\""+outputContent+"\""}]}}
		]}
		return out
def partitionList(list_a, chunk_size):
	for i in range(0, len(list_a), chunk_size):
		yield list_a[i:i + chunk_size]

def convertRhinoMeshtoTriMesh(rhinoMesh, transform=None):
	import trimesh
	if transform == None:
		transform = [0,0,0]
	v_i = 0
	vertices = []
	while v_i < len(rhinoMesh.Vertices):
		v = rhinoMesh.Vertices[v_i]
		# print(v_i, v)
		vertices.append([v.X+transform[0],v.Y+transform[1],v.Z+transform[2]])
		v_i += 1

	faces = []
	for f_i, f in enumerate(rhinoMesh.Faces):
		# print("face",f_i, f)
		faces.append([f[0],f[1],f[2]])
		if f_i >= len(rhinoMesh.Faces)-1:
			break
	mesh = trimesh.Trimesh(vertices=vertices, faces=faces)
	return mesh
def packGeom(request, payload={}):
	import time
	import trimesh
	log=[]
	start_time = time.time()
	name = "packMono"
	structure = {
		"Python": {"version":str(sys.version), "info":str(sys.version_info)}, "Category": "Hops", "Subcategory": "Hops Python", "Uri": "/"+name, "Name": name, "Nickname": name, "Description": name,
		"Inputs": [
			# {"Name": "url", "Nickname": "url", "Description": "url", "ParamType": "Text", "ResultType": "System.String", "Default":None, "AtLeast": 1, "AtMost": 2147483647},
			{"Name": "majorGrid", "Nickname": "M", "Description": "majorGrid", "ParamType": "Number", "ResultType": "System.Double", "Default":None, "AtLeast": 1, "AtMost": 2147483647},
			{"Name": "majorBounds", "Nickname": "B", "Description": "majorBounds", "ParamType": "Mesh", "ResultType": "Rhino.Geometry.Mesh", "Default":None, "AtLeast": 1, "AtMost": 1},
			{"Name": "subGeometry", "Nickname": "S", "Description": "subGeometry", "ParamType": "Text", "ResultType": "System.String", "Default":None, "AtLeast": 1, "AtMost": 2147483647},
		],
		"Outputs": [{"Name": "Log", "Nickname": "L", "Description": "Log", "ParamType": "Text", "ResultType": "System.String", "AtLeast": 1, "AtMost": 1},
			{"Name": "Output", "Nickname": "O", "Description": "Output", "ParamType": "Text", "ResultType": "System.String", "AtLeast": 1, "AtMost": 1},
		]}
	if request.method =="GET":	return JsonResponse(structure)
	if payload != {}:
		grid = list(partitionList(payload["majorGrid"], 3))
		sub_Geom = list(map(lambda x: get_object_or_404(geometryObject, name=x).data["geometry"], payload["subGeometry"]))

		sub_Geom =	list(map(lambda y:
						list(map(lambda x: _coerce_value(x["type"],x["data"]), y))
					, sub_Geom))
		print(sub_Geom)
		# for d in dir(sub_Geom[0]):
			# print(d)
		# print (sub_Geom[0].Translate.__doc__)
		# print(rhino3dm.Intersection.__doc__)
		meshes = []
		transforms = []
		collisions = trimesh.collision.CollisionManager()
		collisions.add_object("-1",convertRhinoMeshtoTriMesh(payload["majorBounds"][0]))

		for index, geom in enumerate(sub_Geom):
			willBreak = False
			for gridPoint in grid:
				# print(gridPoint)
				# geom.Translate(rhino3dm.Vector3d(4000,1000,0))
				temp_collision = trimesh.collision.CollisionManager()
				hard = geom[0]
				soft = geom[1]
				soft_mesh = convertRhinoMeshtoTriMesh(soft,gridPoint)
				
				temp_collision.add_object(str(index),soft_mesh)
				if collisions.in_collision_other(temp_collision):
					# print(gridPoint, "collide")
					pass
				else:
					transforms.append(gridPoint)
					hard_mesh = convertRhinoMeshtoTriMesh(hard,gridPoint)
					collisions.add_object(str(index),hard_mesh)
					willBreak = True
					if willBreak:
						break
		# print(transforms)

				# meshes.append(mesh)
			# collisions.add_object(str(index),mesh)
		# print(collisions.__doc__)
		# print(collisions.in_collision_internal(True,False))
		log.append("--- %s seconds ---" % (time.time() - start_time))
		log = json.dumps(list(map(lambda x: str(x), log)))
		outputContent = json.dumps(transforms)
		out = {"values": [
			{"ParamName": "Log", "InnerTree": {"0": [{"type": "System.String", "data": "\""+log+"\""}]}},
			{"ParamName": "Output", "InnerTree": {"0": [{"type": "System.String", "data": "\""+outputContent+"\""}]}}
		]}
		return out

def objectCRUD(request, payload={}, log=[]):
	name = "objectCRUD"
	structure = {
		"Python": {"version":str(sys.version), "info":str(sys.version_info)}, "Category": "Hops", "Subcategory": "Hops Python", "Uri": "/"+name, "Name": name, "Nickname": name, "Description": name,
		"Inputs": [
			# {"Name": "url", "Nickname": "url", "Description": "url", "ParamType": "Text", "ResultType": "System.String", "Default":None, "AtLeast": 1, "AtMost": 2147483647},
			{"Name": "modelClass", "Nickname": "C", "Description": "modelClass", "ParamType": "Text", "ResultType": "System.String", "Default":None, "AtLeast": 1, "AtMost": 2147483647},
			{"Name": "identifiers", "Nickname": "I", "Description": "identifiers", "ParamType": "Text", "ResultType": "System.String", "Default":None, "AtLeast": 1, "AtMost": 2147483647},
			{"Name": "defaults", "Nickname": "D", "Description": "defaults", "ParamType": "Text", "ResultType": "System.String", "Default":None, "AtLeast": 1, "AtMost": 2147483647},
			{"Name": "geometry", "Nickname": "G", "Geometry": "defaults", "ParamType": "Mesh", "ResultType": "Rhino.Geometry.Mesh", "Default":None, "AtLeast": 1, "AtMost": 2147483647},
			# {"Name": "geometry", "Nickname": "G", "Geometry": "defaults", "ParamType": "Geometry", "ResultType": "Rhino.Geometry.Curve", "Default":None, "AtLeast": 1, "AtMost": 2147483647, "Default": None},

		],
		"Outputs": [{"Name": "Log", "Nickname": "L", "Description": "Log", "ParamType": "Text", "ResultType": "System.String", "AtLeast": 1, "AtMost": 1},
			{"Name": "Output", "Nickname": "O", "Description": "Output", "ParamType": "Text", "ResultType": "System.String", "AtLeast": 1, "AtMost": 1},
		]}
	if request.method =="GET":	return JsonResponse(structure)
	if payload != {}:
		# print(payload)
		import json
		from itertools import cycle
		geometry_o = payload["geometry_original"]
		for modelClass, kwargs, defaults in zip(cycle(payload["modelClass"]), payload["identifiers"], cycle(payload["defaults"])):
			print(modelClass, kwargs, defaults)
			print(type(modelClass), type(kwargs), type(defaults))
			print(type(geometry_o), geometry_o)
			# for d in dir(geometry):
				# print(d)
			# print("-"*100)
			# for d in dir(rhino3dm):
				# print(d)


			if "data" not in defaults:
				defaults["data"] = {}
			defaults["data"]["geometry"] = geometry_o
			kwargs["defaults"] = defaults
			modelInstance = getattr(sys.modules[__name__], modelClass)
			objectInstance, created = modelInstance.objects.update_or_create(**kwargs)
			try:
				print(objectInstance.data)
			except: pass
		outputContent = json.dumps({})
		out = {"values": [
			{"ParamName": "Log", "InnerTree": {"0": [{"type": "System.String", "data": "\""+str(log)+"\""}]}},
			{"ParamName": "Output", "InnerTree": {"0": [{"type": "System.String", "data": "\""+outputContent+"\""}]}}
		]}
		return out