from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("process/<int:id>", views.process, name="process"),
]
