from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import SubjectViewSet, FlashcardViewSet, StudyScheduleViewSet, StudySessionViewSet

router = DefaultRouter()
router.register(r'subjects', SubjectViewSet)
router.register(r'flashcards', FlashcardViewSet)
router.register(r'schedule', StudyScheduleViewSet, basename='schedule')
router.register(r'sessions', StudySessionViewSet, basename='sessions')

urlpatterns = [
    path('', include(router.urls)),
]
