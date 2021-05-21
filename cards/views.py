from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from .models import Card
from .serializers import CardSerializer, CardPostSerializer
from .permissions import IsOwnerOrReadOnly
from django.http import Http404
from matir_bank import response_maker

class CarList(APIView):
    """
    List all cards or create new instance.
    """
    serializer_class = CardSerializer
    permission_classes = [IsAuthenticated, IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    def get(self, request, format=None):
        cards = Card.objects.filter(user=request.user)
        # cards = Card.objects.all()
        serializer = CardSerializer(cards, many=True)
        return response_maker.Ok(serializer.data)

    def post(self, request, format=None):
     
        request.data._mutable = True
        request.data['user'] = request.user.id

        serializer = CardPostSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return response_maker.Ok(serializer.data)
            
        return response_maker.Error(serializer.errors)

class SingleCard(APIView):
    """
    Retrieve, update or delete a card instance.
    """
    serializer_class = CardSerializer
    permission_classes = [IsAuthenticated, IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]
    
    

    def get_object(self, pk, user_id):
        try:
            card = Card.objects.get(pk=pk)
            
            if card.user_id != user_id:
                return None
            
            return card
            
        except Card.DoesNotExist:
            return None

    def get(self, request, pk, format=None):
        card = self.get_object(pk, request.user.id)

        if not card:
            return response_maker.NotFound({"detail": "Not found."})

        serializer = CardSerializer(card)
        return response_maker.Ok(serializer.data)

    def put(self, request, pk, format=None):
        card = self.get_object(pk, request.user.id)
        
        if not card:
            return response_maker.NotFound({"detail": "Not found."})
        
        request.data._mutable = True
        request.data['user'] = request.user.id
        
        serializer = CardPostSerializer(card, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return response_maker.Ok(serializer.data)
        return response_maker.Error(serializer.errors)
    
    def delete(self, request, pk, format=None):
        card = self.get_object(pk, request.user.id)
        if not card:
            return response_maker.NotFound({"detail": "Not found."})
        card.delete()
        return response_maker.Ok({"detail": "Deleted"})