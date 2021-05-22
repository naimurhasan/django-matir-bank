from matir_bank.core import response_maker
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import IdCard
from .serializers import IdCardSerializer, IdCardMutationSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
import os
# Create your views here.

class SingleIdCard(APIView):
    """
    Retrieve, update or delete a card instance.
    """
    serializer_class = IdCardSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        id_cards = IdCard.objects.filter(user=request.user)
        
        id_card = {'user': request.user, 'id': None, 'type': None, 'image': None}
        if(len(id_cards) > 0):
            id_card = id_cards[0]
        
        serializer = IdCardSerializer(id_card, many=False)
        return response_maker.Ok(serializer.data)

    def post(self, request, format=None):
        
        request.data._mutable = True
        request.data['user'] = request.user.id

        serializer = IdCardMutationSerializer(data=request.data)
        if serializer.is_valid():

            id_cards = IdCard.objects.filter(user=request.user)
            
            # create new
            if(len(id_cards) < 1):
                serializer.save()
                return response_maker.Ok(serializer.data, status=status.HTTP_201_CREATED)
            else:
                # update existing
                id_card = id_cards[0]
                serializer = IdCardMutationSerializer(id_card, data=request.data)
                serializer.is_valid()

                os.remove(id_card.image.path)

                serializer.save()
                return response_maker.Ok(serializer.data)

        return response_maker.Error(serializer.errors)