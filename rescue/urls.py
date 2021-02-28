from django.conf.urls import url
from django.urls import path

from rescue import views

urlpatterns = [
    url(r'^$', views.index, name="index"),
    path('download_articles/<int:project>', views.download_articles, name="download_articles"),
    ]
