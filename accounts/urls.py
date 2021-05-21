from .login_register_views import RegisterAPI, LoginAPI
from .views import AccountOverview, SingleAccount
from django.urls import path
from knox import views as knox_views

urlpatterns = [
    path('register/', RegisterAPI.as_view(), name='register'),
    path('login/', LoginAPI.as_view(), name='login'),
    path('logout/', knox_views.LogoutView.as_view(), name='logout'),
    path('logoutall/', knox_views.LogoutAllView.as_view(), name='logoutall'),
    # '' meansa /accounts/
    path('', AccountOverview.as_view(), name='account-overview'),
    #  means /accounts/phone
    path('<str:phone>/', SingleAccount.as_view(), name='account-name'),

]