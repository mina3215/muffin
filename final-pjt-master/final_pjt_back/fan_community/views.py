from django.shortcuts import render
from .models import Actor, Actor_comment
from .serializers import ActorSerializer, Is_ActorSerializer, ActorListSerializer, ActorCommetSerializer
from movies.models import Movie
from movies.serializers import MovieListSerializer

from accounts.models import User, Prize
from accounts.serializers import UserSerializer

from django.shortcuts import get_list_or_404, get_object_or_404
from rest_framework.response import Response
from rest_framework.decorators import api_view

from rest_framework.decorators import permission_classes
from rest_framework.permissions import IsAuthenticated

from rest_framework import status
from django.db.models import Count
# Create your views here.

# 기본으로 표시할 배우들. 한 10명? 팔로우 많은 순으로 처리.
@api_view(['GET'])
def recommend_actors(request):
    excluded_actor_ids = [314159265359]  # 제외하고 싶은 배우 아이디 목록
    actors = Actor.objects.annotate(fan_count=Count('fan')).exclude(id__in=excluded_actor_ids).order_by('-fan_count')
    serializer = ActorListSerializer(actors, many=True)
    return Response(serializer.data[:10])


# 배우 정보, 배우 게시판..?
@api_view(['GET'])
def actor_detail(request, actor_id, username):
    user = get_object_or_404(User, username=username)
    actor = get_object_or_404(Actor, pk=actor_id)
    if actor in user.like_actor.all():
        actor_serializer = Is_ActorSerializer(actor)
    else:
        actor_serializer = ActorSerializer(actor)

    # 배우가 출연한 영화
    actor_movies = actor.movie.all()
    movies_serializer = MovieListSerializer(actor_movies, many=True)
    data = {
        'movies': movies_serializer.data,
        'actor' : actor_serializer.data
    }
    return Response(data)


# 배우 팔로우
@api_view(['POST'])
def follow_actor(request, actor_id):
    actor = get_object_or_404(Actor, pk=actor_id)
    user = get_object_or_404(User, username=request.data['username'])
    prize = get_object_or_404(Prize, pk=1)
    easter_prize = get_object_or_404(Prize, pk=3)
    
    if user in actor.fan.all():
        actor.fan.remove(user)
        serializer = ActorSerializer(actor)
    else:
        actor.fan.add(user)
        serializer = Is_ActorSerializer(actor)
        if prize not in user.prize_of_user.all():
            user.prize_of_user.add(prize)
        if easter_prize not in user.prize_of_user.all() and actor_id == 314159265359 :
            user.prize_of_user.add(easter_prize)
    return Response(serializer.data)

    
@api_view(['POST','GET'])
def actor_comment_create(request, actor_pk):
    if request.method == 'GET':
        Comments = get_list_or_404(Actor_comment, actor = actor_pk)
        serializer = ActorCommetSerializer(Comments, many=True)    
        return Response(serializer.data)
    
    if request.method == 'POST':
        user = get_object_or_404(User, username=request.data['author'])
        actor = get_object_or_404(Actor, pk=actor_pk)
        prize = get_object_or_404(Prize, pk = 4)
        comments_cnt = Actor_comment.objects.filter(actor=actor_pk, author=user.id).count()
        comments_data = {
                'content': request.data['content'],
                'author': user.id,
                'actor': actor.id
            }
        serializer = ActorCommetSerializer(data=comments_data)

        get_first_4 = 0
        if prize not in user.prize_of_user.all() and comments_cnt==10:
            user.prize_of_user.add(prize)
            get_first_4 = 1

        if serializer.is_valid(raise_exception=True):
            serializer.save()
            data = {
                'comments' : serializer.data,
                'get_first_4' : get_first_4 
            }
            return Response(data, status=status.HTTP_201_CREATED)
    