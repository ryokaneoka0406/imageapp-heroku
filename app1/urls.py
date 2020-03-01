from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("process/<str:code>", views.process, name="process"),
    path("about", views.about, name="about"),
    path("example", views.example, name="example"),
]
