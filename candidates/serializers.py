from rest_framework import serializers
from .models import Candidate

class CandidateSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Candidate
        fields = ('id', 'title', 'first_name', 'last_name')