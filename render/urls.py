from django.urls import path

from . import views

urlpatterns = [
    # path('', views.index, name='index'),    
    path("favicon/", views.favicon, name="favicon"),   
    path("", views.index, name="index"),
    path("triangles/<slug:slug>", views.generate, name="generate")
]