from django.urls import path

from . import views

urlpatterns = [
    path('', views.inspection, name='index'),
    path('inspection/', views.inspection, name='inspection'),
]
