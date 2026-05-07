import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from study.models import Subject, Flashcard

def seed():
    # Create Subjects
    react, _ = Subject.objects.get_or_create(name="React", color="#61dbfb", description="Frontend framework")
    python, _ = Subject.objects.get_or_create(name="Python", color="#3776ab", description="Backend language")
    sql, _ = Subject.objects.get_or_create(name="SQL", color="#00758f", description="Database queries")

    # Create Flashcards
    Flashcard.objects.get_or_create(
        subject=react,
        question="O que é o Virtual DOM?",
        answer="É uma representação leve do DOM real que o React usa para otimizar atualizações."
    )
    Flashcard.objects.get_or_create(
        subject=python,
        question="O que são List Comprehensions?",
        answer="Uma forma concisa de criar listas em Python usando uma única linha de código."
    )
    Flashcard.objects.get_or_create(
        subject=sql,
        question="Qual a diferença entre INNER JOIN e LEFT JOIN?",
        answer="INNER JOIN retorna apenas registros com correspondência em ambas as tabelas. LEFT JOIN retorna todos da tabela à esquerda."
    )
    print("Seeding complete!")

if __name__ == "__main__":
    seed()
