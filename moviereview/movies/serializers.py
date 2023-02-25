from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Movie,Review

class MovieSerializer(serializers.Serializer):
    name=serializers.CharField()
    ticket_price=serializers.IntegerField()
    genre=serializers.CharField()

class UserModelSerializer(serializers.ModelSerializer):
    class Meta:
        model=User
        fields=['username','password','email']
        def create(self,validated_data):
            return User.objects.create_user(**validated_data)
class MovieModelSer(serializers.ModelSerializer):
    class Meta:
        model=Movie
        fields="__all__"
    def validate(self,data):
        cost=data.get("ticket_price")
        if cost<0:
            raise serializers.ValidationError
        return data
class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model=Review
        fields=[
            'review',
            'rating',
            'date'
        ]
    def create(self,validated_data):
        user=self.context.get("user")
        movie=self.context.get("movie")
        return Review.objects.create(user=user,movie=movie,**validated_data)