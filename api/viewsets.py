from rest_framework import viewsets

from api import models, serializers

class MachineViewSet(viewsets.ModelViewSet):
    queryset = models.Machine.objects.all()
    serializer_class = serializers.MachineSerializer

class CommandViewSet(viewsets.ModelViewSet):
    queryset = models.Command.objects.all()
    serializer_class = serializers.CommandSerializer

class CommandOptionsViewSet(viewsets.ModelViewSet):
    queryset = models.CommandOptions.objects.all()
    serializer_class = serializers.CommandOptionsSerializer