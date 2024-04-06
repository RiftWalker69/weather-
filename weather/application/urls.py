from django.urls import path
from . import views

urlpatterns = [
    path('', views.application, name='application'),
    path('second/',views.map_view,name='map')
]