from django.urls import path
from . import views

urlpatterns = [
    path('<str:username>/follow/', views.follow),
    path('<str:username>/<str:requestername>/',views.user_detail),
    path('<int:author>/',views.getusername),

]
