from django.db import models
from django.utils import timezone

class Subject(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    color = models.CharField(max_length=20, default="#3b82f6") # Default blue

    def __str__(self):
        return self.name

class Flashcard(models.Model):
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name='flashcards')
    question = models.TextField()
    answer = models.TextField()
    is_learned = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    # Spaced Repetition Fields (SM-2 Algorithm)
    next_review = models.DateTimeField(default=timezone.now)
    interval = models.IntegerField(default=1) # in days
    ease_factor = models.FloatField(default=2.5)
    repetitions = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.subject.name} - {self.question[:20]}"

class StudySchedule(models.Model):
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name='schedules')
    day_of_week = models.IntegerField() # 0 = Monday, ..., 6 = Sunday

    class Meta:
        unique_together = ('subject', 'day_of_week')

    def __str__(self):
        days = ["Segunda", "Terça", "Quarta", "Quinta", "Sexta", "Sábado", "Domingo"]
        return f"{self.subject.name} na {days[self.day_of_week]}"

class StudySession(models.Model):
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name='sessions')
    duration_minutes = models.IntegerField(default=25)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.duration_minutes}m of {self.subject.name} on {self.created_at.date()}"
