from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('graph/', views.graph, name='graph'),
    path('results/', views.results, name='results'),
    path('datasets/', views.datasets, name='datasets'),
    path('datasets/view', views.view, name='view'),
]
