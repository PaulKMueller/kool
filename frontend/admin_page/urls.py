from django.urls import path

from . import views


urlpatterns = [
    path('', views.adminpage, name='admin_page'),
    path('add_entries/', views.add_entries, name='add_entries'),
    path('edit_database/', views.edit_database, name='edit_database'),
    path('change_database/', views.change_database, name='change_database'),
    path('scraper/', views.scraper, name='scraper'),
    path('playground/', views.playground, name='playground'),
]
