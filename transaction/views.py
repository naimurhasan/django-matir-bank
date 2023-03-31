from matir_bank.core.charge_calculator import send_money_charge
from matir_bank.core import response_maker
from cards.models import Card
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import get_user_model
User = get_user_model()


from .models import Transaction
from accounts.models import Account
from .serializers import ( TransactionSerializer,
                            SendMoneySerializer,
                            AddFundSerializer,
                            TopUpSerializer,)
from decimal import Decimal
from datetime import datetime
from django.http import Http404
# for or query
from django.db.models import Q
from matir_bank.core import reserved_accounts
from matir_bank.core import transaction_type
from django.utils import timezone

# Create your views here.
class TransactionView(APIView):
    """
    Retrive, Create Transaction
    """
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        transactions = Transaction.objects.filter(Q(source=request.user.id) | Q(destination=request.user.id))

        serializer = TransactionSerializer(transactions, many=True)

        return response_maker.Ok(serializer.data)


class SingleTransaction(APIView):
    """
    Retrieve transaction instance.
    """
    permission_classes = [IsAuthenticated]

    def get_object(self, pk, user_id):
        try:
            transaction = Transaction.objects.get(pk=pk)
            # Return None if This Transaction Doesn't belong to logged in user
            if transaction.destination != user_id and transaction.source != user_id:
                return None
            
            return transaction
            
        except Transaction.DoesNotExist:
            return None

    def get(self, request, pk, format=None):
        transaction = self.get_object(pk, request.user.id)

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
            
            # check if the card exist
            try:
                card = Card.objects.get(pk=serializer.validated_data['card_id'])
                
                if card.user_id != request.user.id:
                    return response_maker.NotFound({'detail': 'Card Not Found'})
  
            except Card.DoesNotExist:
                return response_maker.NotFound({'detail': 'Card Not Found'})
            
            # check if card has the amount
            try:
                card_account = User.objects.get(pk=reserved_accounts.CARD_USER_ID)
                if card_account.balance < serializer.validated_data['amount']:
                    return response_maker.Error({'detail': 'Not Enough Balance in System.'})

            except:
                return response_maker.Error({'detail': 'Card_Account Not Found'})

            transaction = serializer.save(source=reserved_accounts.CARD_USER_ID, destination=request.user.id, type=transaction_type.CARD)
            
            # update user balance
            request.user.balance = request.user.balance+Decimal(serializer.validated_data['amount'])
            request.user.balance_last_update = datetime.now()
            request.user.save()

            # update card balance
            card_account.balance = card_account.balance - Decimal(serializer.validated_data['amount'])
            card_account.balance_last_update = datetime.now()
            card_account.save()
            

            tserializer = TransactionSerializer(transaction)
            return response_maker.Ok(tserializer.data)

        return response_maker.Error(serializer.errors)

class SendMoney(APIView):
    """ SEND MONEY TO OTHER PERSONAL ACCOUNT"""

    serializer_class = SendMoneySerializer
    permission_classes = [IsAuthenticated]


    def post(self, request, format=None):
        
        serializer = SendMoneySerializer(data=request.data);
        if not serializer.is_valid():
            return response_maker.Error(serializer.errors) 

        # check if have balance more than amount+chard
        money_amount = Decimal(serializer.validated_data['amount'])
        send_chrarge = send_money_charge(money_amount)
        if request.user.balance < money_amount + send_chrarge :
            return response_maker.Error({'detail': 'Not Enough Balance.'})

        # if self destination
        if request.user.id == int(serializer.validated_data['destination']):
            return response_maker.Error({'detail': 'Can not send to self.'})

        # check if destination exist
        #  check if desination is a personal
        try:
            destination = Account.objects.get(phone=serializer.validated_data['destination'])
            if destination.type != 'PERSONAL':
                return response_maker.Error({'detail': 'You can only send money to personal account.'})

        except Account.DoesNotExist:
            return response_maker.Error({'detail': 'Destination does not exist.'})
        
        #  send money to charge account
        try:
            charge_acc = Account.objects.get(pk=reserved_accounts.CHARGE_USER_ID)
        except Account.DoesNotExist:
            return response_maker.Error({'detail': 'Could not found charge account.'})
        
        # save transaction
        transaction = serializer.save(source=request.user.id, type=transaction_type.BALANCE)

        # calculatate both balance
        request.user.balance = request.user.balance - (money_amount+send_chrarge)
        destination.balance = destination.balance + money_amount
        charge_acc.balance = charge_acc.balance + send_chrarge


        # last upate both
        request.user.balance_last_update = timezone.now()
        destination.balance_last_update = timezone.now()
        charge_acc.balance_last_update = timezone.now()

        # save both
        request.user.save()
        destination.save()
        charge_acc.save()
        ctransaction = Transaction(source=request.user.id, destination=charge_acc.id, amount=send_chrarge, type=transaction_type.CHARGE)
        ctransaction.save()

      
        tserializer = TransactionSerializer(transaction)

        return response_maker.Ok(tserializer.data)

class MobileTopup(APIView):
    """
    DO MOBILE TOPUP
    """

    serializer_class = TopUpSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request, format=None):
        serializer = TopUpSerializer(data=request.data)
        if serializer.is_valid():

            # check if have balance
            if request.user.balance < Decimal(serializer.validated_data['amount']):
                return response_maker.Error({'detail': 'Not Enough Balance.'})

             # save transaction
            serializer.save()

            # calculatate both balance
            request.user.balance = request.user.balance-Decimal(serializer.validated_data['amount'])
            
            # last upate both
            request.user.balance_last_update = datetime.now()
            
            # save both
            request.user.save()

            return response_maker.Ok(serializer.data)

        return response_maker.Error(serializer.errors)

