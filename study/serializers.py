from rest_framework import serializers
from .models import Subject, Flashcard

class SubjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subject
        fields = '__all__'

class FlashcardSerializer(serializers.ModelSerializer):
    subject_name = serializers.ReadOnlyField(source='subject.name')

    class Meta:
        model = Flashcard
        fields = '__all__'
