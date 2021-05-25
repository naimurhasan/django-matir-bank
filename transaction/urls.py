from django.urls import path
from rest_framework.permissions import IsAuthenticated

from . import views

urlpatterns = [
    path('', views.TransactionView.as_view(), name="transaction-list"),
    path('do/send-money/', views.SendMoney.as_view(), name="transaction-instance"),
    path('do/add-fund/', views.AddFundView.as_view(), name='add-fund'),
    path('do/top-up/', views.MobileTopup.as_view(), name="topup"),
    path('<str:pk>/', views.SingleTransaction.as_view(), name="transaction-instance"),

]