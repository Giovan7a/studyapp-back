from rest_framework import serializers
from .models import Subject, Flashcard, StudySchedule, StudySession

class SubjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subject
        fields = '__all__'

class FlashcardSerializer(serializers.ModelSerializer):
    subject_name = serializers.CharField(source='subject.name', read_only=True)

    class Meta:
        model = Flashcard
        fields = '__all__'

class StudyScheduleSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudySchedule
        fields = '__all__'

class StudySessionSerializer(serializers.ModelSerializer):
    subject_name = serializers.CharField(source='subject.name', read_only=True)
    subject_color = serializers.CharField(source='subject.color', read_only=True)

    class Meta:
        model = StudySession
        fields = '__all__'
