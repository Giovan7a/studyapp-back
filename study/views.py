from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.utils import timezone
from datetime import timedelta
from django.db.models import Sum
from .models import Subject, Flashcard, StudySchedule, StudySession
from .serializers import SubjectSerializer, FlashcardSerializer, StudyScheduleSerializer, StudySessionSerializer

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
        due = self.request.query_params.get('due')
        
        if subject_id:
            queryset = queryset.filter(subject_id=subject_id)
        if is_learned:
            queryset = queryset.filter(is_learned=is_learned.lower() == 'true')
        if due and due.lower() == 'true':
            queryset = queryset.filter(next_review__lte=timezone.now())
            
        return queryset

    @action(detail=True, methods=['post'])
    def review(self, request, pk=None):
        flashcard = self.get_object()
        score = request.data.get('score')
        
        if score is None:
            return Response({"error": "Score is required"}, status=status.HTTP_400_BAD_REQUEST)
            
        try:
            score = int(score)
        except ValueError:
            return Response({"error": "Score must be an integer"}, status=status.HTTP_400_BAD_REQUEST)

        if score < 0 or score > 5:
            return Response({"error": "Score must be between 0 and 5"}, status=status.HTTP_400_BAD_REQUEST)

        # SuperMemo-2 Algorithm
        if score >= 3:
            if flashcard.repetitions == 0:
                flashcard.interval = 1
            elif flashcard.repetitions == 1:
                flashcard.interval = 6
            else:
                flashcard.interval = int(flashcard.interval * flashcard.ease_factor)
            flashcard.repetitions += 1
        else:
            flashcard.repetitions = 0
            flashcard.interval = 1
            
        flashcard.ease_factor = flashcard.ease_factor + (0.1 - (5 - score) * (0.08 + (5 - score) * 0.02))
        if flashcard.ease_factor < 1.3:
            flashcard.ease_factor = 1.3
            
        flashcard.next_review = timezone.now() + timedelta(days=flashcard.interval)
        flashcard.save()
        
        serializer = self.get_serializer(flashcard)
        return Response(serializer.data)

class StudyScheduleViewSet(viewsets.ModelViewSet):
    queryset = StudySchedule.objects.all()
    serializer_class = StudyScheduleSerializer

    @action(detail=False, methods=['get'])
    def today(self, request):
        today_idx = timezone.now().weekday()
        schedules = StudySchedule.objects.filter(day_of_week=today_idx)
        
        total_subjects = schedules.count()
        completed_subjects = 0
        
        subjects_data = []
        for schedule in schedules:
            subject = schedule.subject
            # Count due flashcards for this subject
            due_cards = Flashcard.objects.filter(
                subject=subject,
                next_review__lte=timezone.now()
            ).count()
            
            if due_cards == 0:
                completed_subjects += 1
                
            subjects_data.append({
                "subject_id": subject.id,
                "subject_name": subject.name,
                "subject_color": subject.color,
                "due_cards": due_cards,
                "is_completed": due_cards == 0
            })
            
        progress = (completed_subjects / total_subjects * 100) if total_subjects > 0 else 0
        
        return Response({
            "day_of_week": today_idx,
            "total_scheduled": total_subjects,
            "completed": completed_subjects,
            "progress_percentage": round(progress),
            "subjects": subjects_data
        })

class StudySessionViewSet(viewsets.ModelViewSet):
    queryset = StudySession.objects.all().order_by('-created_at')
    serializer_class = StudySessionSerializer

    @action(detail=False, methods=['get'])
    def stats(self, request):
        now = timezone.now()
        # Tempo total nos ultimos 7 dias
        last_7_days = now - timedelta(days=7)
        sessions_7d = StudySession.objects.filter(created_at__gte=last_7_days)
        total_minutes = sessions_7d.aggregate(total=Sum('duration_minutes'))['total'] or 0
        
        # Agrupado por matéria
        subject_stats = []
        for subject in Subject.objects.all():
            minutes = sessions_7d.filter(subject=subject).aggregate(total=Sum('duration_minutes'))['total'] or 0
            if minutes > 0:
                subject_stats.append({
                    "subject_name": subject.name,
                    "subject_color": subject.color,
                    "minutes": minutes
                })

        return Response({
            "total_minutes_last_7_days": total_minutes,
            "subject_stats": subject_stats
        })
