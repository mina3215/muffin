from django.urls import path
from . import views

urlpatterns = [
    # path('<str:username>/follow/', views.follow),
    # 배우 페이지로 이동 -> follow 버튼, 이름, 출연 작... 표시...
    path('actorpage/', views.recommend_actors),
    path('follow/<int:actor_id>', views.follow_actor),
    path('detail/<int:actor_id>/<str:username>/', views.actor_detail),

    # path('comments/<int:actor_pk>/', views.actor_comment_list),
    path('createcomments/<int:actor_pk>/', views.actor_comment_create),
]
