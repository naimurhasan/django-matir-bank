from django.shortcuts import render
from django.http import JsonResponse
from rest_framework import status    
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from .models import Card
from .serializers import CardSerializer
from api import serializers
from rest_framework.permissions import IsAuthenticated
# Create your views here.

@api_view(('GET',))
def apiOverview(request):
    api_urls = {
        'Card':'/cards',
    }

    return Response(api_urls)

@api_view(('GET',))
@permission_classes((IsAuthenticated, ))
def cardList(request):
    cards = Card.objects.all()
    serializer = CardSerializer(cards, many=True)
    return Response(serializer.data)
    
@api_view(('GET',))
def cardDetail(request, pk):
    try:
        card = Card.objects.get(id=pk)
    except ValueError:
       return Response({'status': 'Must Be Integer'}, status=status.HTTP_400_BAD_REQUEST)
    except Card.DoesNotExist:
        return Response({'status': 'Not Found'}, status=status.HTTP_404_NOT_FOUND)

    serializer = CardSerializer(card, many=False)
    return Response(serializer.data)

@api_view(('POST',))
def cardCreate(request):
    serializer = CardSerializer(data=request.data)

    if serializer.is_valid():
        serializer.save()

    return Response(serializer.data)

@api_view(('POST',))
def cardUpdate(request, pk):
    try:
        card = Card.objects.get(id=pk)
    except ValueError:
       return Response({'status': 'Must Be Integer'}, status=status.HTTP_400_BAD_REQUEST)
    except Card.DoesNotExist:
        return Response({'status': 'Not Found'}, status=status.HTTP_404_NOT_FOUND)

    serializer = CardSerializer(instance=card, data=request.data)

    if serializer.is_valid():
        serializer.save()

    return Response(serializer.data)

@api_view(('DELETE',))
def cardDelete(request, pk):
    try:
        card = Card.objects.get(id=pk)
    except ValueError:
       return Response({'status': 'Must Be Integer'}, status=status.HTTP_400_BAD_REQUEST)
    except Card.DoesNotExist:
        return Response({'status': 'Not Found'}, status=status.HTTP_404_NOT_FOUND)

    card.delete();

   
    return Response({'status': 'Item Deleted Successfully.'})