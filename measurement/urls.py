from django.urls import path
from .views import *

app_name= 'measurement'

urlpatterns = [
    path('', calculate_des_view, name='calculate-view'),
]
