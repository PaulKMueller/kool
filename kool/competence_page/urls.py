from django.urls import path

from . import views

urlpatterns = [
    path('', views.competence_page),
    path('cs', views.cs_page)
]
