from matir_bank.core import response_maker
from accounts.models import Account
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.core import serializers
from django.http import Http404
from django.conf import settings
from matir_bank.core.hostname import get_current_host
from photos.serializers import PhotoPathSerializer, PhotoSerializer

class AccountOverview(APIView):
    """
    Retrieve, update or delete a account info
    """
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        user = request.user
        photo = user.photo_set.all()[:1].values() if user.photo_set.all()[:1] else None
        photoData = None

        if photo != None:
            photoData = {}
            photoData['image'] = get_current_host(request)[:-1]+settings.MEDIA_URL+photo[0]['image']
            photoData['created_at'] = photo[0]['created_at']
            photoData['updated_at'] = photo[0]['updated_at']

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
            'photo':  photoData
        }

        return response_maker.Ok(account)


class SingleAccount(APIView):
    """
    Retrieve name of phone.
    """
    permission_classes = [IsAuthenticated]

    def get_object(self, phone):
        try:
            account = Account.objects.get(phone=phone)
            
            return account
            
        except Account.DoesNotExist:
            raise Http404

    def get(self, request, phone, format=None):
        account = self.get_object(phone)

        photo = account.photo_set.all()[:1].values()[0]  if account.photo_set.all()[:1] else None
        
        if photo != None:
            photo['image'] = get_current_host(request)[:-1]+settings.MEDIA_URL+photo['image']
            photo.pop('id')
            photo.pop('user_id')
            

        return response_maker.Ok({
            'id': account.id,
            'name': account.name,
            'photo':  photo
            })