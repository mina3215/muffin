from django.shortcuts import render
from .models import User, Prize

from fan_community.serializers import ActorListSerializer
from movies.serializers import MovieListSerializer
from django.shortcuts import get_object_or_404, get_list_or_404
from .serializers import UserSerializer, is_UserSerializer, PrizeSerializer
from rest_framework.response import Response
from rest_framework.decorators import api_view

# from rest_framework.decorators import permission_classes
# from rest_framework.permissions import IsAuthenticated
# Create your views here.
@api_view(['GET'])
def user_detail(request, username, requestername):
    user = get_object_or_404(User, username=username) 
    requester = User.objects.get(username=requestername)
    # print(user.like_movies)
    playList=MovieListSerializer(user.like_movies, many=True)
    
    prizes = user.prize_of_user.all()
    prizes_serializer = PrizeSerializer(prizes, many=True)
    actors = user.like_actor.all()
    actors = ActorListSerializer(actors, many=True)

    if requester in user.followers.all():    
        serializer = is_UserSerializer(user)
        # print('1',serializer.data)
    else:
        serializer = UserSerializer(user)
        # print('2',serializer.data)
    data = {
        'user' : serializer.data,
        'playList' : playList.data,
        'prizes' : prizes_serializer.data,
        'actors' : actors.data
    }
    return Response(data)

# def 

# @permission_classes([IsAuthenticated])
@api_view(['POST','GET'])
def follow(request, username):
    person = get_object_or_404(User, username=username)
    user = User.objects.get(username=request.data["user"])
    if user in person.followers.all():
        person.followers.remove(user)
        serializer = UserSerializer(person)    
    else:
        person.followers.add(user)
        serializer = is_UserSerializer(person)
    return Response(serializer.data)
    

@api_view(['GET'])
# author는 작성자id를 뜻함, axios 넘겨줄때, 정수값으로 넘겨주면 됨
def getusername(request, author):
    user = get_object_or_404(User, pk=author)
    serializer = UserSerializer(user)
    return Response(serializer.data)