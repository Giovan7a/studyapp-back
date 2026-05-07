from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import SubjectViewSet, FlashcardViewSet

router = DefaultRouter()
router.register(r'subjects', SubjectViewSet)
router.register(r'flashcards', FlashcardViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
