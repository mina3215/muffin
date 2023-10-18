from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.conf import settings
# Create your models here.

class Genre(models.Model):
    name = models.CharField(max_length = 100)

class Movie(models.Model):
    title = models.CharField(max_length = 100)
    release_date = models.DateField()
    popularity = models.FloatField()
    vote_count = models.IntegerField()
    vote_average = models.FloatField()
    overview = models.TextField()
    poster_path = models.TextField()
    original_language = models.CharField(max_length = 100)
    genre_ids = models.ManyToManyField(Genre, related_name='movie_of_genre')
    like_users = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='like_movies')
    video_path = models.TextField()
    jamo = models.CharField(max_length = 100)

# class movie_genre(models.Model):
    
class Boxoffice(models.Model):
    rank = models.IntegerField()
    # movie = models.OneToOneField(Movie, on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)


class Comment(models.Model):
    score = models.FloatField(validators=[MinValueValidator(0),MaxValueValidator(5)])
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    content = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Review(models.Model):
    title = models.CharField(max_length=100)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    like_users = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='like_articles')
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class ReviewComment(models.Model):
    review = models.ForeignKey(Review, on_delete=models.CASCADE, related_name='comments')
    parent_comment = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='replies') #답글 기능을 구현하기 위해 추가
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    content = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    like_users = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='liked_comments')
