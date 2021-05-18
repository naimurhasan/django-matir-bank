
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from .models import Card
from .serializers import CardSerializer
from .permissions import IsOwnerOrReadOnly
from django.http import Http404

class CarList(APIView):
    """
    List all cards or create new instance.
    """
    serializer_class = CardSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    def get(self, request, format=None):
        # cards = Card.objects.filter(user=request.user)
        cards = Card.objects.all()
        serializer = CardSerializer(cards, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
     
        request.data._mutable = True
        request.data['user'] = request.user.id

        serializer = CardSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
            # return Response(request.user.id)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class SingleCard(APIView):
    """
    Retrieve, update or delete a card instance.
    """
    serializer_class = CardSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]
    
    def get_object(self, pk, user_id):
        try:
            card = Card.objects.get(pk=pk)
            
            if card.user_id != user_id:
                raise Http404
            
            return card
            
        except Card.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        card = self.get_object(pk, request.user.id)
        serializer = CardSerializer(card)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        card = self.get_object(pk, request.user.id)
        
        
        request.data._mutable = True
        request.data['user'] = request.user.id
        
        serializer = CardSerializer(card, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, pk, format=None):
        card = self.get_object(pk, request.user.id)
        card.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)