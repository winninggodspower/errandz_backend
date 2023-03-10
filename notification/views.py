from django.shortcuts import render
from .serializers import registerDeviceNotificationTokenSerializer
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

# Create your views here.

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def registerDeviceNotificationTokenView(request):
    serializer = registerDeviceNotificationTokenSerializer(data = request.data)
    serializer.is_valid(raise_exception=True)
    serializer.save(account=request.user)
    return Response(serializer.data, status=status.HTTP_200_OK)


