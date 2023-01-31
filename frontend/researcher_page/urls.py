from django.urls import path

from . import views

urlpatterns = [
    path('<int:id>', views.researcher, name='homepage'),
    path('', views.researcher, name='homepage'),
    path('change_status', views.change_status_researcher,
         name='change_status_researcher')
]