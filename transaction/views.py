from matir_bank import response_maker
from cards.models import Card
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from .models import Transaction
from accounts.models import Account
from .serializers import TransactionSerializer, TransactionPostSerializer, AddFundSerializer
from decimal import Decimal
from datetime import datetime
from django.http import Http404
# for or query
from django.db.models import Q

# Create your views here.
class TransactionView(APIView):
    """
    Retrive, Create Transaction
    """
    serializer_class = TransactionPostSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        transactions = Transaction.objects.filter(Q(source=request.user.phone) | Q(destination=request.user.phone))

        serializer = TransactionSerializer(transactions, many=True)

        return response_maker.Ok(serializer.data)

    def post(self, request, format=None):
        
        serializer = TransactionPostSerializer(data=request.data);
        if not serializer.is_valid():
            return response_maker.Error(serializer.errors) 

        # check if have balance more than amount
        if request.user.balance < Decimal(serializer.validated_data['amount']):
            return response_maker.Error({'detail': 'Not Enough Balance.'})

        # if self destination
        if request.user.id == int(serializer.validated_data['destination']):
            return response_maker.Error({'detail': 'Can not send to self.'})

        # check if destination exist
        try:
            destination = Account.objects.get(phone=serializer.validated_data['destination'])
            
        except Account.DoesNotExist:
            return response_maker.Error({'detail': 'Destination does not exist.'})
        
        # save transaction
        serializer.save(source=request.user.phone, type="Balance")

        # calculatate both balance
        request.user.balance = request.user.balance-Decimal(serializer.validated_data['amount'])
        destination.balance = destination.balance+Decimal(serializer.validated_data['amount'])
        
        # last upate both
        request.user.balance_last_update = datetime.now()
        destination.balance_last_update = datetime.now()

        # save both
        request.user.save()
        destination.save()

        return response_maker.Ok(serializer.data)

class SingleTransaction(APIView):
    """
    Retrieve transaction instance.
    """
    permission_classes = [IsAuthenticated]

    def get_object(self, pk, user_phone):
        try:
            transaction = Transaction.objects.get(pk=pk)
            
            if transaction.destination != user_phone and transaction.source != user_phone:
                return None
            
            return transaction
            
        except Transaction.DoesNotExist:
            return None

    def get(self, request, pk, format=None):
        transaction = self.get_object(pk, request.user.phone)

        if not transaction:
            return response_maker.NotFound({"detail": "Not found."})

        serializer = TransactionSerializer(transaction)
        return response_maker.Ok(serializer.data)
    

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
                    return response_maker.NotFound({'detail': 'Card Not Found'})
  
            except Card.DoesNotExist:
                return response_maker.NotFound({'detail': 'Card Not Found'})

            
            serializer.save(destination=request.user.phone, type='Card')
            request.user.balance = request.user.balance+Decimal(request.data['amount'])
            request.user.balance_last_update = datetime.now()
            request.user.save()
            return response_maker.Ok(serializer.data, status=status.HTTP_201_CREATED)

        return response_maker.Error(serializer.errors)