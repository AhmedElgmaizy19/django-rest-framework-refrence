from rest_framework import serializers
from .models import *

class MoveSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movie
        fields = '__all__'


class GuestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Guest
        fields = ['pk','reversition', 'name' , 'mobile' ]


class RversitionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reversition
        fields = '__all__'

class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = '__all__'