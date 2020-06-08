from .models import *
from rest_framework import serializers

class buildingComponentSerializer(serializers.ModelSerializer):
	data = serializers.JSONField()
	class Meta:
		model = buildingComponent
		exclude = (
			'createdFunction',
			'enableDelete',
			'errorText',
			'hasError',
			'created',
			'updated',
		)
