from matir_bank.core.hostname import get_current_host
from matir_bank.core import response_maker
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Photo
from .serializers import PhotoSerializer, PhotoMutationSerializer, PhotoPathSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
import os
# Create your views here.

class SinglePhoto(APIView):
    """
    Retrieve, update or delete a photo instance.
    """
    serializer_class = PhotoSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        photos = Photo.objects.filter(user=request.user)
        
        photo = {'user': request.user, 'id': None, 'image': None}
        if(len(photos) > 0):
            photo = photos[0]
            
        serializer = PhotoPathSerializer(photo, many=False, context={'request': request})
        return response_maker.Ok(serializer.data)

    def post(self, request, format=None):
        
        request.data._mutable = True
        request.data['user'] = request.user.id

        serializer = PhotoMutationSerializer(data=request.data)
        if serializer.is_valid():

            photos = Photo.objects.filter(user=request.user)
            
            # create new
            if(len(photos) < 1):
                serializer.save()
                return response_maker.Ok(serializer.data)
            else:
                # update existing
                photo = photos[0]
                serializer = PhotoMutationSerializer(photo, data=request.data)
                serializer.is_valid()

                os.remove(photo.image.path)

                serializer.save()
                return response_maker.Ok(serializer.data)

        return response_maker.Error(serializer.errors)