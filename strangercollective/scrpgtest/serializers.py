from .models import *
from rest_framework import serializers


class CharacterSerializer(serializers.Serializer):
	id = serializers.IntegerField(read_only=True)
	firstname = serializers.CharField(required=False, allow_blank=True, max_length=100)