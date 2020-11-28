from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include
from . import views

app_name = "APP"

urlpatterns = [
    path("", views.index, name="index"),
    path("homepage.html", views.index, name="index"),
    path("index.html", views.login, name="login"),
    path("Home.html", views.convert, name="convert"),
    path("register.html", views.register, name="register"),



]
