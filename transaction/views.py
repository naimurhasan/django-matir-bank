from django.db.models.fields import DecimalField
from cards.models import Card
from django.db import models
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from .models import Transaction
from .serializers import TransactionSerializer, AddFundSerializer
from django.http import Http404
from decimal import Decimal
# Create your views here.
class TransactionView(APIView):
    """
    Retrive, Create Transaction
    """
    serializer_class = TransactionSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        transactions = Transaction.objects.all()

        serializer = TransactionSerializer(transactions, many=True)

        return Response(serializer.data)

    def post(self, request, format=None):
        
        serializer = TransactionSerializer(data=request.data);
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST) 

        # check if have balance more than amount
        if request.user.balance < int(request.data['amount']):
            return Response({'detail': 'Not Enough Balance.'}, status=status.HTTP_400_BAD_REQUEST)

        # check if destination exist
        
        # mutate transaction source

        # save transaction 

        # calculatate balance

        return Response('OK')

class AddFundView(APIView):
    """
    Add Fund
    """

    serializer_class = AddFundSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request, format=None):

        serializer = AddFundSerializer(data=request.data)
        
        if serializer.is_valid():
            
            # check if the card exit
            try:
                card = Card.objects.get(pk=serializer.validated_data['card_id'])
                
                if card.user_id != request.user.id:
                    return Response({'detail': 'Card Not Found'}, status=status.HTTP_400_BAD_REQUEST)
  
            except Card.DoesNotExist:
                return Response({'detail': 'Card Not Found'}, status=status.HTTP_400_BAD_REQUEST)

            
            serializer.save(destination=request.user.phone, type='Card')
            request.user.balance = request.user.balance+Decimal(request.data['amount'])
            request.user.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)