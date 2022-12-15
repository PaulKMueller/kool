from django.urls import path

from . import views

urlpatterns = [
    path('', views.categories_page),
    path('biology', views.competence_page),
    path('chemistry', views.competence_page),
    path('cs', views.competence_page),
    path('economics', views.competence_page)
]
