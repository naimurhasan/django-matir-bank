from django.urls import path

from . import views

urlpatterns = [
    path('', views.SingleIdCard.as_view(), name="idcard-instance"),
]