from django.urls import path

from . import views

urlpatterns = [
    path('', views.SinglePhoto.as_view(), name="photo-instance"),
]