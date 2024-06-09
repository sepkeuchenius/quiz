from fastui import components as c
from models import Question, Option, Answer


def render_question(question: Question):
    return [
        c.Paragraph(text=question.text),
        *[c.Image(media) for media in question.media],
        *[c.Paragraph(text=f"{option.value.value}: {option.text}") for option in question.options]
    ]


def q_wielrenner(prev_answer: str):
    return Question(
        text=f"Let's go {prev_answer.title()}! Welke wielrenner werd ook wel de das genoemd?",
        options=[Option(text='Michiel Tournier', value=Answer.a), Option(text='Sep Keuchenius', value=Answer.b)],
        answer=Answer.a
    )
    


QUESTIONS = [
    q_wielrenner
]

def get_question(index, prev_answer = None):
    return render_question(QUESTIONS[index](prev_answer)) if index < len(QUESTIONS) else None
