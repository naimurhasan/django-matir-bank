from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Photo
from .serializers import PhotoSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
import os
# Create your views here.

class SinglePhoto(APIView):
    """
    Retrieve, update or delete a card instance.
    """
    serializer_class = PhotoSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        photos = Photo.objects.filter(user=request.user)
        
        photo = {'user': request.user, 'id': None, 'image': None}
        if(len(photos) > 0):
            photo = photos[0]
        
        serializer = PhotoSerializer(photo, many=False)
        return Response(serializer.data)

    def post(self, request, format=None):
        
        request.data._mutable = True
        request.data['user'] = request.user.id

        serializer = PhotoSerializer(data=request.data)
        if serializer.is_valid():

            photos = Photo.objects.filter(user=request.user)
            
            # create new
            if(len(photos) < 1):
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            else:
                # update existing
                photo = photos[0]
                serializer = PhotoSerializer(photo, data=request.data)
                serializer.is_valid()

                os.remove(photo.image.path)

                serializer.save()
                return Response(serializer.data)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)