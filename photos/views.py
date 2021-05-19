from rest_framework.response import Response
from rest_framework.views import APIView

# Create your views here.

class SinglePhoto(APIView):
    """
    Retrieve, update or delete a card instance.
    """

    def get(self, request, format=None):
        return Response("OK")