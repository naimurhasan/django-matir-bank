from rest_framework.response import Response
from rest_framework.decorators import api_view

@api_view(('GET',))
def apiOverview(request):
    api_urls = {
        'Card':'/cards',
    }

    return Response(api_urls)
