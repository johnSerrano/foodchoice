from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index, name="index"),
    url(r'^request', views.request, name="request"),
    url(r'^result', views.result, name="result"),
    url(r'^restaurants', views.show_restaurants, name="show_restaurants"),
]
