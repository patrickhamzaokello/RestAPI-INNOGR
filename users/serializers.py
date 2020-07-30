from rest_framework import serializers
from .models import Profile

class Profileserializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Profile
        fields = ('image','description','phone','firstSkill','secondSkill','thirdSkill')