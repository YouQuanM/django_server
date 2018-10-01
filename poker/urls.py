from django.conf.urls import url, include
import views

urlpatterns = [
    url(r'add_player$', views.add_player, ),
]

