from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('text_received', views.text_received, name='text_received'),
]
