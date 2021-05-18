from django.urls import path

from . import views

urlpatterns = [
    path('', views.apiOverview, name="api-overview"),
    path('cards/', views.cardList, name="card-list"),
    path('cards/create', views.cardCreate, name="card-create"),
    path('cards/<str:pk>', views.cardDetail, name="card-detail"),
    path('cards/<str:pk>/update', views.cardUpdate, name="card-update"),
    path('cards/<str:pk>/delete', views.cardDelete, name="card-update"),
]
