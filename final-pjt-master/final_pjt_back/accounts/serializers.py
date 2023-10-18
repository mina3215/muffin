from rest_framework import serializers
from .models import User, Prize

class UserSerializer(serializers.ModelSerializer):
    
    follower_cnt = serializers.SerializerMethodField()
    followings_cnt = serializers.SerializerMethodField()
    is_follow = serializers.BooleanField(default=False)

    def get_follower_cnt(self, obj):
        return obj.followers.count()
    
    def get_followings_cnt(self, obj):
        return obj.followings.count()
    
    class Meta:
        model = User
        fields = ('first_name','last_name','username','follower_cnt','followings_cnt', 'is_follow', 'like_movies')
        
class is_UserSerializer(UserSerializer):
    is_follow = serializers.BooleanField(default=True)
    class Meta(UserSerializer.Meta):
        pass
    
class PrizeSerializer(serializers.ModelSerializer):
    class Meta():
        model = Prize
        fields = '__all__'