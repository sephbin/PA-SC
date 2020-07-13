from .models import *
from rest_framework import serializers


serializelist = ['race','campaign','status', 'characterType']
for s in serializelist:
	class TempSerializer(serializers.ModelSerializer):
		class Meta:
			model = globals()[s]
			fields = ('__all__')
	globals()[s+'Serializer'] = TempSerializer

class AdvantageSerializer(serializers.ModelSerializer):
		class Meta:
			model = advantage
			fields = ('__all__')

class RelAdvantageSerializer(serializers.ModelSerializer):
		advantage = AdvantageSerializer(read_only=True)
		cost = serializers.IntegerField()
		name = serializers.CharField()
		class Meta:
			model = rel_advantage
			fields = ('__all__')

class DisadvantageSerializer(serializers.ModelSerializer):
		class Meta:
			model = disadvantage
			fields = ('__all__')

class RelDisadvantageSerializer(serializers.ModelSerializer):
		disadvantage = DisadvantageSerializer(read_only=True)
		cost = serializers.IntegerField()
		name = serializers.CharField()
		class Meta:
			model = rel_disadvantage
			fields = ('__all__')

class SkillSerializer(serializers.ModelSerializer):
		class Meta:
			model = skill
			fields = ('__all__')

class RelSkillSerializer(serializers.ModelSerializer):
		skill = SkillSerializer(read_only=True)
		cost = serializers.IntegerField()
		skill_challenge = serializers.CharField()
		skill_attribute = serializers.CharField()
		relative_skill = serializers.CharField()
		relative_value = serializers.IntegerField()
		class Meta:
			model = rel_skill
			fields = ('__all__')

class PossessionSerializer(serializers.ModelSerializer):
		class Meta:
			model = possession
			# fields = ('__all__')
			exclude= (
				'meleeStatsText',
				'rangeStatsText',
				'armourStatsText',
					)

class RelPossessionSerializer(serializers.ModelSerializer):
		possession = PossessionSerializer(read_only=True)
		cost = serializers.IntegerField()
		weight = serializers.FloatField()
		meleeStats = serializers.ListField()
		rangeStats = serializers.ListField()
		class Meta:
			model = rel_possession
			fields = ('__all__')


class CharacterSerializer(serializers.ModelSerializer):
	race = raceSerializer(read_only=True)
	status = statusSerializer(read_only=True)
	displayname = serializers.CharField()
	cost = serializers.JSONField()
	# characterType = characterTypeSerializer(read_only=True)
	reladvantage = RelAdvantageSerializer(read_only=True, many=True)
	reldisadvantage = RelDisadvantageSerializer(read_only=True, many=True)
	relskill = RelSkillSerializer(read_only=True, many=True)
	relpossession = RelPossessionSerializer(read_only=True, many=True)
	possessionTotals = serializers.JSONField()
	meleePossessions = RelPossessionSerializer(read_only=True, many=True)
	rangePossessions = RelPossessionSerializer(read_only=True, many=True)
	# damage = serializers.DictField()
	# cost = serializers.IntegerField()
	class Meta:
		model = character
		fields = ('__all__')

		# fields = ('id', 'firstname', 'race', 'advantages')

class CharacterSerializer_Updated(serializers.ModelSerializer):
	class Meta:
		model = character
		fields = ('updated',)


class CampaignSerializer(serializers.ModelSerializer):
		character = CharacterSerializer(read_only=True, many=True)
		possession = PossessionSerializer(read_only=True, many=True)
		class Meta:
			model = campaign
			fields = ('__all__')



class skill_Serializer(serializers.ModelSerializer):
		class Meta:
			model = skill
			fields = ('__all__')


class rel_skill_template_ListSerializer(serializers.ListSerializer):
	class Meta:
		model = rel_skill_template
	@classmethod
	def many_init(cls, *args, **kwargs):
		# Instantiate the child serializer.
		kwargs['child'] = cls()
		# Instantiate the parent list serializer.
		return rel_skill_template_ListSerializer(*args, **kwargs)
	def create(self, validated_data):
		print("rel_skill_template_ListSerializer","create")
		outs = [rel_skill_template(**item) for item in validated_data]
		return rel_skill_template.objects.bulk_create(outs)
	def update(self, instance, validated_data):
		from django.shortcuts import get_object_or_404
		# Maps for id->instance and id->data item.
		print("rel_skill_template_ListSerializer","update")
		print(instance)
		print(validated_data)
		print("..1")
		# ob_mapping = {ob.id: ob for ob in instance}
		print("..12")
		data_mapping = {item['id']: item for item in validated_data}
		print("..13")

		# Perform creations and updates.
		print("..2")
		ret = []
		for ob_id, data in data_mapping.items():
			print(ob_id, data)
			try:
				ob = get_object_or_404(instance,id=ob_id)
				ret.append(self.child.update(ob, data))
				print("..21")
			except:
				ret.append(self.child.create(data))
				print("..22")

		# Perform deletions.
		# for ob_id, ob in ob_mapping.items():
		# 	if ob_id not in data_mapping:
		# 		ob.delete()

		print("..3")
		return ret



def createOb(staticSelf, validated_data):
	import json
	for nest in staticSelf.nestedLUT:
		try:
			nested_data = validated_data.pop(nest["key"])
			elementModel = getattr(sys.modules[__name__], nest["model"])
			serializerModel = getattr(sys.modules[__name__], nest["serializer"])
			serializedObject = serializerModel(data = nested_data, many=nest["many"])
			if serializedObject.is_valid():
				savedObject = serializedObject.save()
			if nest["many"]:
				pass
			else:
				validated_data[nest["key"]]= serializedObject.data
		except Exception as e:
			print("serializer create:",e)
			pass
	outOb = characterTemplate.objects.create(**validated_data)
	return outOb

def updateOb(staticSelf, instance, validated_data):
	import json
	for nest in staticSelf.nestedLUT:
		try:
			print("1")
			print("instance",instance)
			nested_data = dict(validated_data.pop(nest["key"]))
			elementModel = getattr(sys.modules[__name__], nest["model"])
			serializerModel = getattr(sys.modules[__name__], nest["serializer"])
			print("2")
			if nest["many"]:
				elementObject = get_object_or_404(elementModel, **search)
				serializedObject = serializerModel(elementObject , data = nested_data, many=nest["many"])
				if serializedObject.is_valid():
					savedObject = serializedObject.save()
			else:
				print(nested_data)
				search = {nest["identifier"]:nested_data[nest["identifier"]]}
				print(search)
				try:
					elementObject = get_object_or_404(elementModel, **search)
					print("FOUND ELEMENTOBJECT")
				except Exception as e:
					serializedObject = serializerModel(data = nested_data)
					print("2.2")
					if serializedObject.is_valid():
						savedObject = serializedObject.save()
						print("savedObject", savedObject, nested_data)
					else:
						validated_data[nest["key"]]= serializedObject.data
					print("5")
		except Exception as e:
			print("serializer update:",e)
			pass
	instClass = instance.__class__
	outOb, created = instClass.objects.update_or_create(id=instance.id, defaults=validated_data)
	print("######",outOb, created, validated_data)
	return outOb

class rel_skill_template_Serializer(serializers.ModelSerializer):
	skill = skill_Serializer(required=False)
	class Meta:
		model = rel_skill_template
		fields = ('id','rank',
			'skill',
			)
		list_serializer_class = rel_skill_template_ListSerializer
	nestedLUT = [
	{"key":"skill", "model":"skill", 'serializer': 'skill_Serializer_skill_name', 'many':False, "identifier":"skill_name"},
	]
	# def create(self, validated_data):
	# 	return createOb(self, validated_data)
	# def update(self, instance, validated_data):
	# 	return updateOb(self, instance, validated_data)

class characterTemplate_Serializer(serializers.ModelSerializer):
	rel_skill_template = rel_skill_template_Serializer(many=True, required=False)
	# skills = skill_Serializer_skill_name(many=True)
	class Meta:
		model = characterTemplate
		fields = ('__all__')

	# nestedLUT = [
	# {"key":"rel_skill_template", "model":"rel_skill_template", 'serializer': 'rel_skill_template_Serializer', 'many':True, "identifier":None},
	# ]
	# # room_type_name = serializers.CharField(source='room_type.type_name', )

	# def create(self, validated_data):
	# 	print("--ctS-c-")
	# 	return createOb(self, validated_data)
	# def update(self, instance, validated_data):
	# 	print("--ctS-u-")
	# 	return updateOb(self, instance, validated_data)