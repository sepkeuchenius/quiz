from fastui import components as c
from models import Question, Option, Answer


def render_question(question: Question):
    return question.text, [
        *[c.Image(media) for media in question.media],
        *[c.Paragraph(text=f"{option.value.value}: {option.text}") for option in question.options]
    ]

QUESTIONS = [
    Question(
        text=f"Welke wielrenner werd ook wel de das genoemd?",
        options=[Option(text='Michiel Tournier', value=Answer.a), Option(text='Sep Keuchenius', value=Answer.b)],
        answer=Answer.a
    )
]

def get_question(index):
    return render_question(QUESTIONS[index]) if index < len(QUESTIONS) else None
