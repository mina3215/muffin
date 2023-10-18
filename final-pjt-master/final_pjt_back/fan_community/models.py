from django.db import models
from django.conf import settings
from movies.models import Movie
# Create your models here.

class Actor(models.Model):
    name = models.CharField(max_length=100)
    profile_path = models.TextField() # NULL값 있음 주의 
    # movie = models.ManyToManyField(Movie, related_name='actor_of_movie')
    fan = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name="like_actor")
    movie = models.ManyToManyField(Movie, related_name="movies_of_actor")
    jamo = models.CharField(max_length=100)


class Actor_comment(models.Model):
    actor = models.ForeignKey(Actor, on_delete=models.CASCADE)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    content = models.TextField()
