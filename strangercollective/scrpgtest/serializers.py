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
			fields = ('__all__')

class RelPossessionSerializer(serializers.ModelSerializer):
		possession = PossessionSerializer(read_only=True)
		cost = serializers.IntegerField()
		weight = serializers.FloatField()
		class Meta:
			model = rel_possession
			fields = ('__all__')

class CharacterSerializer(serializers.ModelSerializer):
	race = raceSerializer(read_only=True)
	campaign = campaignSerializer(read_only=True)
	status = statusSerializer(read_only=True)
	characterType = characterTypeSerializer(read_only=True)
	reladvantage = RelAdvantageSerializer(read_only=True, many=True)
	reldisadvantage = RelDisadvantageSerializer(read_only=True, many=True)
	relskill = RelSkillSerializer(read_only=True, many=True)
	relpossession = RelPossessionSerializer(read_only=True, many=True)
	possessionTotals = serializers.DictField()
	class Meta:
		model = character
		fields = ('__all__')

		# fields = ('id', 'firstname', 'race', 'advantages')