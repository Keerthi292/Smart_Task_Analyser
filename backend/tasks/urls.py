from django.urls import path
from .views import analyze_tasks, home

urlpatterns = [
    path("", home),              # 👈 this makes the homepage work
    path("analyze/", analyze_tasks),
]