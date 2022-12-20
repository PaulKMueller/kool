from django.urls import path

from . import views

urlpatterns = [
    path('', views.abstract_page),
    path('<int:id>/detailed/<int:auth_id>',
         views.abstract_page)
]
