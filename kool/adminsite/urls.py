from django.urls import path

from . import views


urlpatterns = [
    path('', views.adminpage, name='adminsite'),
    path('add_entries/', views.add_entries, name='add_entries')
]
