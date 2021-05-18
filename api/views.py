from rest_framework.response import Response
from rest_framework.decorators import api_view

@api_view(('GET',))
def apiOverview(request):
    api_urls = {
        'Card [List, Create]':'/cards',
        'Card [Single]':'/cards/<int:id>',
        "Accounts: [Register]" : "accounts/register/",
        "Accounts: [Login]" : "accounts/login/",
        "Accounts: [Logout]" : "accounts/logout/",
        "Accounts: [Logout All]" : "accounts/logoutall/"
    }

    return Response(api_urls)
