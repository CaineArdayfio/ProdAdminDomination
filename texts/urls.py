from django.urls import path

from . import views

urlpatterns = [
    path('send_product_to_phone', views.send_product_to_phone,
         name='send_product_to_phone'),
    path('text_received', views.text_received, name='text_received'),
]
