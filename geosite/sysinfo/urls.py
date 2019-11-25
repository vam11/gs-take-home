from django.urls import path
from geosite.sysinfo import views

urlpatterns = [
    path('', views.Index.as_view()),
    path('api/<int:pk>/', views.API.as_view()),
]
