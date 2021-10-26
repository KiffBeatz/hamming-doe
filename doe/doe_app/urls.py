from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('graph/', views.graph, name='graph'),
    path('datasets/', views.datasets, name='datasets'),
    path('datasets/view', views.view, name='view'),
    path('datasets/format', views.format, name='format'),
    #path('stores/<int:store_id>/',stores_views.detail),
]
