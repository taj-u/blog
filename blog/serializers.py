from rest_framework import serializers
from .models import Post 

class PostSerializer(serializers.ModelSerializer):
    class Meta:
        Model = Post
        fields = ('title', 'slug', 'author', 'publish', 'tags', 'body')