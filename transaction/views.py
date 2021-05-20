from cards.models import Card
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from .models import Transaction
from .serializers import TransactionSerializer, AddFundSerializer
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
    serializer_class = TransactionSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        transactions = Transaction.objects.filter(Q(source=request.user.phone) | Q(destination=request.user.phone))

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

class SingleTransaction(APIView):
    """
    Retrieve transaction instance.
    """
    permission_classes = [IsAuthenticated]

    def get_object(self, pk, user_phone):
        try:
            transaction = Transaction.objects.get(pk=pk)
            
            if transaction.destination != user_phone and transaction.source != user_phone:
                raise Http404
            
            return transaction
            
        except transaction.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        transaction = self.get_object(pk, request.user.phone)
        serializer = TransactionSerializer(transaction)
        return Response(serializer.data)
    

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
            request.user.balance_last_update = datetime.now()
            request.user.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)