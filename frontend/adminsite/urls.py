from django.urls import path

from . import views


urlpatterns = [
    path('', views.adminpage, name='adminsite'),
    path('add_entries/', views.add_entries, name='add_entries'),
    path('edit_database/', views.edit_database, name='edit_database'),
    path('rebuild/', views.rebuild, name='rebuild'),
    path('scraper/', views.scraper, name='scraper'),
    path('playground/', views.playground, name='playground'),
]
