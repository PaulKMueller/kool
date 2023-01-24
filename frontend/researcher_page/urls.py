from django.urls import path
from . import views

urlpatterns = [
    path('', views.researcher_page),
    path('<int:id>/detailed/<int:auth_id>',
         views.researcher_page),
    path('<int:id>/detailed/',
         views.researcher_page),
    path('<int:id>/detailed',
         views.researcher_page)
]
