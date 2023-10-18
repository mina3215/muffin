# from django.db import models
# from django.contrib.auth.models import AbstractUser
from django.db import models
from django.contrib.auth.models import AbstractUser

# # Create your models here.
class User(AbstractUser):
    followings = models.ManyToManyField('self', symmetrical=False, related_name='followers')
    # 좋아요
    # 플레이리스트
    class Meta:
        swappable = 'AUTH_USER_MODEL'
        
class Prize(models.Model):
    prize_title = models.TextField()
    prize_content = models.TextField()
    user = models.ManyToManyField(User, related_name="prize_of_user")
    