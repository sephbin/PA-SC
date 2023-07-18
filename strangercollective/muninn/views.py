from .models import *
from .serializers import *
from rest_framework import viewsets, filters
from django_filters.rest_framework import DjangoFilterBackend
import sys
class parentViewSet(viewsets.ModelViewSet):
	pass

print("HELLO!")
print(parentModel.__subclasses__())
for subclass in parentModel.__subclasses__():
	print("Hello")
	try:
		vsName = str(subclass.__name__)+"_viewSet"
		serName = str(subclass.__name__)+"_serializer"
		vsOb = getattr(sys.modules[__name__], vsName)
		qs = subclass.objects.filter(enabled=True)
		ser = getattr(sys.modules[__name__], serName)
		# vsOb.queryset = qs
		print(vsName)
		# test = type(vsName, (parentViewSet,),{"queryset":qs, "serializer_class":ser,})
		print(test)
		# globals()[vsName]
	except Exception as e:
		print(e)
		pass
class geometry_viewset(viewsets.ModelViewSet):
	queryset = geometry.objects.filter(enabled=True)
	serializer_class = geometry_serializer
	filter_backends = [filters.OrderingFilter, filters.SearchFilter , DjangoFilterBackend, ]
	filterset_fields = {'geometry':['exact'],'updated':['gte', 'lte', 'exact', 'gt', 'lt'],'created':['gte', 'lte', 'exact', 'gt', 'lt']}
	search_fields = ('$geometry',)
	ordering_fields = '__all__'
	ordering = ['createdBy','pk',]

# class containerViewSet(viewsets.ModelViewSet):
	# queryset = container.objects.filter(enabled=True)
	# serializer_class = containerSerializer_read
	# filter_backends = [filters.OrderingFilter, filters.SearchFilter , DjangoFilterBackend, ]
	# filterset_fields = ['project__identifier','elementCategory__name', 'container__elementId', 'elementId',]
	# search_fields = ('$data',)
	# ordering_fields = '__all__'
	# ordering = ['name',]
	# renderer_classes = tuple(api_settings.DEFAULT_RENDERER_CLASSES) + (drfrenderer.CSVRenderer, )