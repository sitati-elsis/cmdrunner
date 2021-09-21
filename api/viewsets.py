import logging

from django.contrib.auth.models import User
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.permissions import AllowAny

from api import models, serializers

logger = logging.getLogger(__name__)

class MachineViewSet(viewsets.ModelViewSet):
    """
    retrieve:
        Return a machine instance.

    list:
        Return all machines.

    create:
        Create a new machine.

    delete:
        Remove an existing machine.

    update:
        Update a machine.
    """
    queryset = models.Machine.objects.all()
    serializer_class = serializers.MachineSerializer


class CommandViewSet(viewsets.ModelViewSet):
    """
    retrieve:
        Return a command instance.

    list:
        Return all commands.

    create:
        Create a new command.

    delete:
        Remove an existing command.

    update:
        Update a command.
    """
    queryset = models.Command.objects.all()
    serializer_class = serializers.CommandSerializer


class CommandOptionsViewSet(viewsets.ModelViewSet):
    """
    retrieve:
        Return a commandoption instance.

    list:
        Return all commandoptions.

    create:
        Create a new commandoption.

    delete:
        Remove an existing commandoption.

    update:
        Update a commandoption.
    """
    queryset = models.CommandOptions.objects.all()
    serializer_class = serializers.CommandOptionsSerializer


class ResultViewSet(viewsets.ModelViewSet):
    """
    retrieve:
        Return a result instance.
        
    list:
        Return all results.
    """
    queryset = models.Result.objects.all()
    serializer_class = serializers.ResultSerializer

class SignupViewSet(viewsets.ViewSet):
    """
    create:
        Create a new user.
    """
    permission_classes = [AllowAny]
    def create(self, request):
        try:
            serializer = serializers.UserSerializer(data=request.data)
            if serializer.is_valid():
                user = User.objects.create_user(**serializer.validated_data)
                user.save()
                message = {
                    'message': 'User signup successful.'
                }
                return Response(message, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            logging.info('Failed to create new user')
            logging.exception(e)
        message = {
            'error': 'Failed to create new user.'
        }
        return Response(message, status=status.HTTP_400_BAD_REQUEST)