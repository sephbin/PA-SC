from .models import *
from rest_framework import serializers


class geometry_serializer(serializers.ModelSerializer):
	geometry = serializers.JSONField()
	class Meta:
		model = geometry
		fields = ('pk', 'geometry')
