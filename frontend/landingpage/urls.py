from django.urls import path

from . import views

urlpatterns = [
    path('', views.home, name='homepage'),
    path('aboutkool/', views.aboutkoolpage, name='aboutkool')
]
