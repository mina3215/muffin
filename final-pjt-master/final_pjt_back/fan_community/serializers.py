from rest_framework import serializers
from .models import Actor, Actor_comment

class ActorSerializer(serializers.ModelSerializer):
    is_follow = serializers.BooleanField(default=False)
    fan_cnt = serializers.SerializerMethodField()

    def get_fan_cnt(self, obj):
        return obj.fan.count()
    class Meta:
        model = Actor
        fields = '__all__'

class Is_ActorSerializer(ActorSerializer):
    is_follow = serializers.BooleanField(default=True)
    class Meta(ActorSerializer.Meta):
        pass

class ActorListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Actor
        fields = '__all__'

class ActorCommetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Actor_comment
        fields = '__all__'