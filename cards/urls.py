from django.urls import path

from . import views

urlpatterns = [
    path('', views.CarList.as_view(), name="card-list"),
    path('<str:pk>/', views.SingleCard.as_view(), name="card-instance"),
]