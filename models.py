from pydantic import BaseModel, Field
import enum
from fastui import components as c

class User(BaseModel):
    answer: str

class Answer(str, enum.Enum):
    a = 'A'
    b = 'B'
    c = 'C'
    d = 'D'


class QuestionForm(BaseModel):
    answer: Answer = Field(title='Kies een antwoord')

class Option(BaseModel):
    text: str
    value: Answer

class Question(BaseModel):
    answer: Answer
    text: str
    media: list[c.Image] | None = Field([])
    options: list[Option] 

