from django.urls import path

from . import views

urlpatterns = [
    path('', views.categories_page),
    path('<int:id>', views.competence_page)
]
