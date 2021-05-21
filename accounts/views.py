from matir_bank import response_maker
from accounts.models import Account
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.core import serializers
from django.http import Http404

class AccountOverview(APIView):
    """
    Retrieve, update or delete a account info
    """
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        user = request.user

        account = {
            'id' : user.id,
            'name': user.name,
            'phone' : user.phone,
            'balance' : user.balance,
            'last_login': user.last_login,
            'created_at': user.created_at,
            'updated_at': user.created_at,
            'balance_last_update': user.balance_last_update,
            'cards': user.card_set.all().values(),
            'photo':  user.photo_set.all()[:1].values() if user.photo_set.all()[:1] else None 
        }

        return response_maker.Ok(account)


class SingleAccount(APIView):
    """
    Retrieve name of phone.
    """
    permission_classes = [IsAuthenticated]

    def get_object(self, phone, user_phone):
        try:
            account = Account.objects.get(phone=phone)
            
            return account
            
        except Account.DoesNotExist:
            raise Http404

    def get(self, request, phone, format=None):
        account = self.get_object(phone, request.user.phone)
        
        return response_maker.Ok({
            'name': account.name,
            'phone': account.phone,
            'photo':  account.photo_set.all()[:1].values() if account.photo_set.all()[:1] else None
            })