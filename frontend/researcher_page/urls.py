from django.urls import path

from . import views

urlpatterns = [
    path('<int:id>', views.researcher, name='homepage'),
    path('', views.researcher, name='homepage'),
]