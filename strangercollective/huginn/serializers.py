from .models import *
from rest_framework import serializers

class RecursiveField(serializers.Serializer):
	def to_representation(self, value):
		serializer = self.parent.parent.__class__(value, context=self.context)
		return serializer.data

class RecursiveTestField(serializers.Serializer):
	def to_representation(self, value):
		print("RecursiveTestField")
		serializer = globals()['ParameterObSerializer'](value, context=self.context)
		return serializer.data

class FunctionObSerializer(serializers.ModelSerializer):
	class Meta:
		model = functionOb
		fields = ('__all__')

class MapSerializer(serializers.ModelSerializer):
	# function = FunctionObSerializer(read_only=True)
	object_from = RecursiveTestField(read_only=True)
	class Meta:
		model = parameterMapThroughObject
		# fields = ('__all__')
		exclude = ('id', 'object_to')

class ParameterObSerializer(serializers.ModelSerializer):
	# sourceParameter = RecursiveField(many=True, read_only=True)
	# groups = serializers.SerializerMethodField('get_maps')
	maps = MapSerializer(source="through_to", many=True)
	# function = RecursiveField(many=True, read_only=True)
	# cost = serializers.IntegerField()
	class Meta:
		model = parameterObject
		fields = ('__all__')

	def get_maps(self, obj):
		qset = obj.object_to
		return [MapSerializer(m).data for m in qset]


class ParameterObSerializer_CU(serializers.ModelSerializer):
	class Meta:
		model = parameterObject
		exclude = ('sourceParameter','param_created_at')

class ParameterMapSerializer_CU(serializers.ModelSerializer):
	class Meta:
		model = parameterMapThroughObject
		exclude = ('map_created_at',)


class TestModelSerializer(serializers.ModelSerializer):
	data = serializers.JSONField()
	class Meta:
		model = testModel
		fields = ('__all__')