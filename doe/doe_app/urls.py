from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='doe-home'),
    path('graph/', views.graph, name='doe-graph'),
]
