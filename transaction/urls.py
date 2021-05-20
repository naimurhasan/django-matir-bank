from django.urls import path
from rest_framework.permissions import IsAuthenticated

from . import views

urlpatterns = [
    path('', views.TransactionView.as_view(), name="transaction-list"),
]