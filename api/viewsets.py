from django.contrib.auth.models import User
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.permissions import AllowAny

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


class ResultViewSet(viewsets.ModelViewSet):
    queryset = models.Result.objects.all()
    serializer_class = serializers.ResultSerializer

class SignupViewSet(viewsets.ViewSet):
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
            print('Failed to create new user')
        message = {
            'error': 'Failed to create new user.'
        }
        return Response(message, status=status.HTTP_400_BAD_REQUEST)