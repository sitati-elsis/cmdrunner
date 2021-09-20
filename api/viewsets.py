from rest_framework import viewsets

from api import models, serializers

class MachineViewSet(viewsets.ModelViewSet):
    queryset = models.Machine.objects.all()
    serializer_class = serializers.MachineSerializer