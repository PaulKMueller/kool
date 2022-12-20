from django.urls import path

from . import views

urlpatterns = [
    path('<int:id>', views.results, name='homepage'),
    path('', views.results, name='homepage')
]