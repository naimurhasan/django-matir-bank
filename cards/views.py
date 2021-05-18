from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from .models import Card
from .serializers import CardSerializer
import json

class CarList(APIView):
    """
    List all cards or create new
    """

    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        cards = Card.objects.filter(user=request.user)
        serializer = CardSerializer(cards, many=True)
        return Response(serializer.data)

    serializer_class = CardSerializer

    def post(self, request, format=None):
        postData = request.data
        postData['user'] = request.user.id
        serializer = CardSerializer(data=postData)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
