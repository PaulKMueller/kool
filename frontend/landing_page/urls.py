from django.urls import path

from . import views

urlpatterns = [
    path('', views.home, name='homepage'),
    path('about_kool/', views.aboutkoolpage, name='about_kool')
]
