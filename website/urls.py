from django.urls import path

from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("galerija/", views.gallery, name="gallery"),
    path("aktuelnosti/", views.news_list, name="news_list"),
    path("aktuelnosti/<slug:slug>/", views.news_detail, name="news_detail"),
    path("video/", views.videos, name="videos"),
    path("partneri/", views.partners, name="partners"),
    path("kontakt/", views.contact, name="contact"),
    path("set-language/", views.set_language, name="set_language"),
]
