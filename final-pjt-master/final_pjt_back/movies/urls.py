# movies/urls.py

from django.urls import path
from . import views

app_name = 'movies'

urlpatterns = [
    path('home/', views.movie_list, name='movie-list'),
    path('comments/<int:movie_pk>/', views.comment_list, name='comment-list'),
    path('comments/<int:movie_pk>/create/', views.comment_create, name='comment-create'),
    
    path('movies/<int:movie_pk>/reviews/', views.review_list, name='review-list'),
    path('detail/<int:movie_pk>/<str:username>/', views.movie_detail),
    
    path('movies/<int:movie_pk>/reviews/<int:pk>/', views.review_detail, name='review-detail'),
    path('like/<int:movie_pk>/', views.like_it),

    path('search/<str:keyword>/', views.search),
    path('recommend/<str:username>/', views.recommend_movie),
    
    path('movies/genre/<int:genre_pk>/', views.genre_movie),
    path('movies/comments/<int:review_pk>/', views.review_comment_list, name='review-comment-list'),
    path('movies/commentsedit/<int:comment_pk>/<int:review_pk>/', views.review_comment_detail, name='review-comment-detail'),
    path('movies/comments/<int:comment_pk>/like/', views.like_review_comment, name='like-review-comment'),

]
