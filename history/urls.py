from django.urls import path
from .views import image_history

urlpatterns = [
    path("history/", image_history),
]