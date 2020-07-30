from rest_framework import serializers
from .models import Post

class Postserializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Post
        fields = ('title','summary','date_posted')