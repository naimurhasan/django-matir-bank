from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Photo
from .serializers import PhotoSerializer
from rest_framework.permissions import IsAuthenticated
# Create your views here.

class SinglePhoto(APIView):
    """
    Retrieve, update or delete a card instance.
    """

    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        photos = Photo.objects.filter(user=request.user)
        
        photo = {'user': request.user, 'id': None, 'image': None}
        if(len(photos) > 0):
            photo = photos[0]
        
        serializer = PhotoSerializer(photo, many=False)
        return Response(serializer.data)

    
