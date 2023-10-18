from django.shortcuts import get_list_or_404, get_object_or_404
from rest_framework.response import Response
from rest_framework.decorators import api_view
from accounts.models import User, Prize
from accounts.serializers import UserSerializer
from hangul_utils import split_syllables, join_jamos

from fan_community.models import Actor
from fan_community.serializers import ActorListSerializer
from accounts.serializers import PrizeSerializer

from django.db.models import Q
from hangul_utils import split_syllables, join_jamos

from rest_framework.decorators import permission_classes
from rest_framework.permissions import IsAuthenticated

from rest_framework import status
from .models import Movie, Boxoffice, Comment, Review, Genre, ReviewComment
from .serializers import MovieListSerializer, MovieSerializer, CommentSerializer, ReviewSerializer, like_MovieSerializer, GenreSerializer, ReviewCommentSerializer
from .algorithm import recommend
import random

@api_view(['GET'])
def movie_list(request):
    movies = get_list_or_404(Boxoffice)
    boxoffice = []
    for movie in movies:
        movie_id = movie.movie_id
        boxoffice.append(get_object_or_404(Movie, pk=movie_id))
    serializer = MovieListSerializer(boxoffice, many = True)
    return Response(serializer.data)

@api_view(['GET'])
def movie_detail(request, movie_pk, username):
    movie = get_object_or_404(Movie, pk=movie_pk)
    user = get_object_or_404(User, username = username)
    actors = movie.movies_of_actor.all()
    # print(actors)
    actors_serializer = ActorListSerializer(actors, many=True)
    if user in movie.like_users.all():
        serializer = like_MovieSerializer(movie)
    else:
        serializer = MovieSerializer(movie)
    data = {
        'movies' : serializer.data,
        'actors' : actors_serializer.data[:4]
    }
    return Response(data)

@api_view(['POST'])
def like_it(request, movie_pk):
    movie = get_object_or_404(Movie, pk=movie_pk)
    user = get_object_or_404(User, username=request.data['user'])
    prize = get_object_or_404(Prize, pk=2)
    if user in movie.like_users.all():
        movie.like_users.remove(user)
        serializer = MovieSerializer(movie)
    else:
        movie.like_users.add(user)
        serializer = like_MovieSerializer(movie)
        if prize not in user.prize_of_user.all():
             user.prize_of_user.add(prize)
    return Response(serializer.data)

@api_view(['GET'])
def genre_movie(request, genre_pk):
    movies = get_list_or_404(Movie, genre_ids=genre_pk)
    genre = get_object_or_404(Genre, pk=genre_pk)
    serializer = MovieListSerializer(movies, many=True)
    genreserializer = GenreSerializer(genre)
    serializer_data = random.sample(serializer.data, 10)

    data = {
        'movies' : serializer_data,
        'genre_name' : genreserializer.data
    }
    return Response(data)
    


@api_view(['GET'])
def comment_list(request,movie_pk):
    if request.method=='GET':
        comments=get_list_or_404(Comment, movie=movie_pk)
        serializer = CommentSerializer(comments, many=True)
        return Response(serializer.data)
    
@api_view(['POST'])
def comment_create(request, movie_pk):
    movie = get_object_or_404(Movie, pk=movie_pk)
    comments_data = {
            'score': request.data.get('score'),
            'content': request.data.get('content'),
            'author': request.user.id,
            'movie': movie_pk
        }
    serializer = CommentSerializer(data=comments_data)
    if serializer.is_valid(raise_exception=True):
        serializer.save(movie = movie)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


@api_view(['GET', 'POST'])
def review_list(request, movie_pk):
    if request.method == 'GET':
        reviews = Review.objects.filter(movie=movie_pk)
        serializer = ReviewSerializer(reviews, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    elif request.method == 'POST':
        movie = get_object_or_404(Movie, pk=movie_pk)
        review_data = {
            'title': request.data.get('title'),
            'content': request.data.get('content'),
            'author': request.user.id,
            'movie': movie_pk
        }
        serializer = ReviewSerializer(data=review_data)
        print(serializer)
        if serializer.is_valid():
            serializer.save()
            print("리뷰 디비 저장 성공")

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'DELETE'])
def review_detail(request, movie_pk, pk):
    try:
        print(request)
        review = Review.objects.get(movie=movie_pk, pk=pk)
    except Review.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = ReviewSerializer(review)
        return Response(serializer.data)
    
    elif request.method == 'PUT':
        serializer = ReviewSerializer(review, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    elif request.method == 'DELETE':
        review.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

@api_view(['GET'])
def search(request, keyword):
    jamo = ''
    for i in keyword:
        if i == ' ':
            continue
        keyword_jamo = split_syllables(i)
        jamo += keyword_jamo[0]

    title_corr = Movie.objects.filter(title__contains=keyword)
    name_corr = Actor.objects.filter(name__contains=keyword)
    if title_corr.count()==0 and name_corr.count()==0:
        title_corr = Movie.objects.filter(jamo__contains=jamo)    
        name_corr = Actor.objects.filter(jamo__contains=jamo)

    serializer = MovieListSerializer(title_corr, many=True)
    actor_serializer = ActorListSerializer(name_corr, many=True)
    data = {
        'movies': serializer.data,
        'actors': actor_serializer.data
    }
    return Response(data)


@api_view(['GET'])
def recommend_movie(request, username):
    me = get_object_or_404(User, username=username)
    prizes = me.prize_of_user.all()
    prize = PrizeSerializer(prizes, many=True)
    me = UserSerializer(me)
    others = UserSerializer(User.objects.exclude(username = username),many=True)
    movies = MovieSerializer(Movie.objects.all(), many=True)
    data = {
        'me': me.data,
        'others' : others.data,
        'movies' : movies.data
    }
    recommends_list, like_genre = recommend(data)
    # print(recommends_list, list(like_genre))
    list = []
    for i in recommends_list:
        list.append(get_object_or_404(Movie, pk=i))
    recommend_movie = MovieListSerializer(list, many=True)
    like_genre = dict(like_genre)
    like_genre = dict(sorted(like_genre.items(), key=lambda x : x[1], reverse=True))
    
    print(prizes)
    n = 10
    if len(recommend_movie.data) < 10:
        n = len(recommend_movie.data)
    print(n)
    data = {
        'recommendation' : random.sample(recommend_movie.data, n),
        'my_Genre' : dict(like_genre),
        'prizes' : prize.data
    }
    # print(data)
    return Response(data)

       
# 여기서부턴 댓글 뷰스
@api_view(['POST','GET'])
def review_comment_list(request, review_pk):

    if request.method == 'GET':
        review_comment = get_list_or_404(ReviewComment, review=review_pk)
        serializer = ReviewCommentSerializer(review_comment, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    elif request.method == 'POST':
        user = get_object_or_404(User,username=request.data['author'])
        comment_data = {
            'title': request.data.get('title'),
            'content': request.data.get('content'),
            'author': user.id,
            'review': review_pk
        }
        serializer = ReviewCommentSerializer(data=comment_data)
        if serializer.is_valid():
            serializer.save()
            print("댓글 디비 저장 성공")
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)









@api_view(['GET', 'PUT', 'DELETE'])
def review_comment_detail(request,comment_pk, review_pk):
    try:
        review_comment = ReviewComment.objects.get(pk= comment_pk, review=review_pk)

        # review_comment = get_list_or_404(ReviewComment, review=review_pk, pk=comment_pk)
        print(review_comment)
    
    except ReviewComment.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = ReviewCommentSerializer(review_comment)
        return Response(serializer.data)
    
    elif request.method == 'PUT':
        print("댓글 수정 시리얼라이저로 가냐?")
        serializer = ReviewCommentSerializer(review_comment, data=request.data)
        print(serializer)

        if serializer.is_valid():
            serializer.save()
            print("댓글 수정 성공")
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    elif request.method == 'DELETE':
        review_comment.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)





@api_view(['POST'])
def like_review_comment(request, movie_pk, comment_pk):
    comment = get_object_or_404(Comment, pk=comment_pk, movie=movie_pk)
    user = request.user
    if user in comment.like_users.all():
        comment.like_users.remove(user)
    else:
        comment.like_users.add(user)
    serializer = CommentSerializer(comment)
    return Response(serializer.data)