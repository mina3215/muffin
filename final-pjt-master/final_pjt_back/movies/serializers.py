from rest_framework import serializers
from .models import Movie, Comment, Review, Genre, ReviewComment

class MovieListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movie
        fields = ('title', 'poster_path','id')

# 나중에 알고리즘 추천받을 때 쓸듯?
class MovieSerializer(serializers.ModelSerializer):
    # 디테일 받아올 때
    is_like = serializers.BooleanField(default=False)
    class Meta:
        model = Movie
        fields = '__all__'

class like_MovieSerializer(MovieSerializer):
    is_like = serializers.BooleanField(default=True)
    class Meta(MovieSerializer.Meta):
        pass



class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = '__all__'


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review  
        exclude = ('like_users',) 

class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = '__all__'
        
class ReviewCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReviewComment
        exclude = ('like_users',)