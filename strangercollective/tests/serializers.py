from rest_framework import serializers
from .models import *

class TokenSerializer(serializers.ModelSerializer):
	data = serializers.JSONField()
	position = serializers.JSONField()
	class Meta:
		model = token
		fields = ('__all__')