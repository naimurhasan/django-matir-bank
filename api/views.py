from rest_framework.response import Response
from rest_framework.decorators import api_view


@api_view(('GET',))
def apiOverview(request):
    api_urls = {
        'Card [List, Create]':'/cards',
        'Card [Update, Delete]':'/cards/<int:id>',
        'Photo [Get, Post]':'/photo',
        'Id Card [Get, Post]':'/id_card',
        'Transaction [List, Create]':'/transaction',
        'Transaction [Details]':'/transaction/<int:id>',
        'Add Fund [Post]':'/add-fund',
        "Accounts: [Get] (Self Account Info)" : "/accounts",
        "Any account name, photo: [Get]" : "/accounts/phone",
        "Accounts: [Register]" : "/accounts/register/",
        "Accounts: [Login]" : "/accounts/login/",
        "Accounts: [Logout]" : "/accounts/logout/",
        "Accounts: [Logout All]" : "/accounts/logoutall/"
    }

    return Response(api_urls)
