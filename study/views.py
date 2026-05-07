from rest_framework import viewsets
from .models import Subject, Flashcard
from .serializers import SubjectSerializer, FlashcardSerializer

class SubjectViewSet(viewsets.ModelViewSet):
    queryset = Subject.objects.all()
    serializer_class = SubjectSerializer

class FlashcardViewSet(viewsets.ModelViewSet):
    queryset = Flashcard.objects.all()
    serializer_class = FlashcardSerializer
    
    def get_queryset(self):
        queryset = Flashcard.objects.all()
        subject_id = self.request.query_params.get('subject')
        is_learned = self.request.query_params.get('is_learned')
        
        if subject_id:
            queryset = queryset.filter(subject_id=subject_id)
        if is_learned:
            queryset = queryset.filter(is_learned=is_learned.lower() == 'true')
            
        return queryset
