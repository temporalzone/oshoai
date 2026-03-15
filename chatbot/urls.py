from django.urls import path
from . import views

urlpatterns = [
    path('', views.chat, name='chat'),
    path('get/', views.get_response, name='get_response'),
    path("quote/", views.daily_quote),
]