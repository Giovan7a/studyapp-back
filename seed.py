import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from study.models import Subject, Flashcard

def seed():
    # Clear existing data
    Flashcard.objects.all().delete()
    Subject.objects.all().delete()
    
    # ENEM Subjects
    subjects_data = [
        ("Matemática", "#ef4444", "Álgebra, Geometria e Funções"),
        ("Química", "#10b981", "Química Orgânica e Inorgânica"),
        ("Biologia", "#22c55e", "Genética e Ecologia"),
        ("História", "#f59e0b", "História do Brasil e Geral"),
        ("Português", "#3b82f6", "Gramática e Literatura"),
        ("Física", "#8b5cf6", "Mecânica, Óptica e Termodinâmica"),
        ("Geografia", "#06b6d4", "Geografia Física e Humana"),
        ("Filosofia", "#ec4899", "Pensamento Clássico e Moderno"),
        ("Sociologia", "#6366f1", "Cultura, Sociedade e Política"),
        ("Língua Estrangeira", "#f43f5e", "Inglês e Espanhol")
    ]

    subjects_map = {}
    for name, color, desc in subjects_data:
        sub, _ = Subject.objects.get_or_create(name=name, color=color, description=desc)
        subjects_map[name] = sub

    # Flashcards examples
    cards = [
        ("Matemática", "Fórmula da área do triângulo equilátero?", "A = (l² * √3) / 4"),
        ("Física", "Qual a segunda lei de Newton?", "F = m * a (Força é igual a massa vezes aceleração)"),
        ("Geografia", "O que é o fenômeno do El Niño?", "Aquecimento anormal das águas do Oceano Pacífico Equatorial."),
        ("Filosofia", "Quem é o autor da frase 'Penso, logo existo'?", "René Descartes"),
        ("Sociologia", "O que é o conceito de Fato Social para Durkheim?", "Maneiras de agir, pensar e sentir que são exteriores ao indivíduo e exercem coerção."),
        ("Química", "O que caracteriza uma base segundo Arrhenius?", "Substância que em solução aquosa libera íons hidroxila (OH-)."),
        ("Língua Estrangeira", "O que significa 'Actually' em inglês?", "Na verdade (um falso cognato).")
    ]

    for sub_name, question, answer in cards:
        Flashcard.objects.create(
            subject=subjects_map[sub_name],
            question=question,
            answer=answer
        )

    print("Full ENEM Seeding complete!")

if __name__ == "__main__":
    seed()
