from django.urls import path, include
from . import views

app_name = "home"   


urlpatterns = [
    path("you/", views.detailView, name="detail"),
    path("you/upload/", views.uploadView, name="upload"),
    # path("upload/", views.uploadView, name="upload"),
    path("", views.homeView, name="homepage"),
    ]   