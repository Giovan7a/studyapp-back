from rest_framework import viewsets
from .models import Subject, Flashcard
from .serializers import SubjectSerializer, FlashcardSerializer

class SubjectViewSet(viewsets.ModelViewSet):
    queryset = Subject.objects.all()
    serializer_class = SubjectSerializer

class FlashcardViewSet(viewsets.ModelViewSet):
    queryset = Flashcard.objects.all()
    serializer_class = FlashcardSerializer
    filterset_fields = ['subject', 'is_learned']
