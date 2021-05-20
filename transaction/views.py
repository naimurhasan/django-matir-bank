from django.db import models
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from .models import Transaction
from .serializers import TransactionSerializer, AddFundPreivewSerializer
from transaction import serializers

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
            return Response({'message': 'Not Enough Balance.'}, status=status.HTTP_400_BAD_REQUEST)

        # check if destination exist
        
        # mutate transaction source

        # save transaction 

        # calculatate balance

        return Response('OK')

class AddFundView(APIView):
    """
    Add Fund
    """

    serializer_class = AddFundPreivewSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request, format=None):

        cards_length = request.user.card_set.all().count()

        if(cards_length < 1):
            return Response({'message': 'Please add a card first.'}, status=status.HTTP_400_BAD_REQUEST)

        request.data._mutable = True
        request.data['source'] = None
        request.data['destination'] = request.user.phone
        request.data['type'] = 'Card'

        serializer = TransactionSerializer(data=request.data)
        
        if serializer.is_valid():
            serializer.save()
            request.user.balance = request.user.balance+int(request.data['amount'])
            request.user.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)