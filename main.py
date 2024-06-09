from fastui import AnyComponent
from fastui import components as c
from fastui.events import GoToEvent
from fastapi import APIRouter
from fastui import AnyComponent, FastUI
from fastui import components as c

from datetime import date

from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from fastui import FastUI, AnyComponent, prebuilt_html, components as c
from fastui.components.display import DisplayMode, DisplayLookup
from questions import QUESTIONS
from fastui.events import GoToEvent, BackEvent, AuthEvent
from fastapi import APIRouter, Depends, Request
from fastui.forms import fastui_form
from typing import Annotated, Literal, TypeAlias
from pydantic import BaseModel, Field
from fastui.auth.shared import fastapi_auth_exception_handling

from auth_user import User

import uvicorn
import questions


app = FastAPI()
fastapi_auth_exception_handling(app)

def page(*components: AnyComponent, title: str | None = None) -> list[AnyComponent]:
    return [
        c.PageTitle(text=f'Scouting Hermansgroep Reunie Quiz — {title}' if title else 'FastUI Demo'),
        c.Page(
            components=[
                *((c.Heading(text=title),) if title else ()),
                *components,
            ],
        ),
        c.Footer(
            extra_text='FastUI Demo',
            links=[
                c.Link(
                    components=[c.Text(text='Github')], on_click=GoToEvent(url='https://github.com/pydantic/FastUI')
                ),
                c.Link(components=[c.Text(text='PyPI')], on_click=GoToEvent(url='https://pypi.org/project/fastui/')),
                c.Link(components=[c.Text(text='NPM')], on_click=GoToEvent(url='https://www.npmjs.com/org/pydantic/')),
            ],
        ),
    ]

router = APIRouter()
import models
@app.get("/api/", response_model=FastUI, response_model_exclude_none=True)
def index(user: Annotated[User, Depends(User.from_request)]) -> list[AnyComponent]:
    """
    User profile page, the frontend will fetch this when the user visits `/user/{id}/`.
    """ 
    return page(
        c.Heading(text=f"Alright {user.name}. Let's go!", level=3), 
        c.Button(text='Start!', on_click=GoToEvent(url='/question/0')),
        title="Reunie Quiz")



@app.get("/api/answer/{index}", response_model=FastUI, response_model_exclude_none=True)
def quiz(answer: str, index: str, user: Annotated[User, Depends(User.from_request)]) -> list[AnyComponent]:
    """
    User profile page, the frontend will fetch this when the user visits `/user/{id}/`.
    """ 
    if user.answers: 
        user.answers[str(index)] = answer
    else:
        user.answers = {str(index): answer}
    token = user.encode_token()
    return [c.FireEvent(event=AuthEvent(token=token, url=f'/question/{int(index) + 1}'))]    

@app.get("/api/question/{index}", response_model=FastUI, response_model_exclude_none=True)
def quiz(index: str, user: Annotated[User, Depends(User.from_request)]) -> list[AnyComponent]:
    """
    User profile page, the frontend will fetch this when the user visits `/user/{id}/`.
    """ 
    if int(index) < 0:
        return [c.FireEvent(event=GoToEvent(url='/'))]
    elif int(index) >= len(QUESTIONS):
        return [c.FireEvent(event=GoToEvent(url='/score'))]
    else:
        title, q = questions.get_question(int(index))
        return page(
            *q,
            c.ModelForm(model=models.QuestionForm, submit_url=f"/answer/{int(index)}", method='GOTO'),
            c.Button(text="Vorige", on_click=GoToEvent(url=f"/question/{int(index)-1}"), class_name='btn btn-secondary btn-light mt-3'), 
            title=title

        )


@app.get("/api/score", response_model=FastUI, response_model_exclude_none=True)
async def score(user: Annotated[User, Depends(User.from_request)]):
    score = 0
    for index, question in enumerate(QUESTIONS):
        if question.answer.value == user.answers[str(index)]:
            score += 1000
    return page(c.Heading(text=f'Jouw score is {score}, {user.name}!', level=3), c.Text(text="Laat dit aan de organisatie zien!"), title="Score")


@app.get("/api/login", response_model=FastUI, response_model_exclude_none=True)
def login():
    return page(
        c.ModelForm(model=models.LoginForm, submit_url='/api/auth/login', display_mode='page')
    )

@app.post("/api/auth/login")
async def login_form_post(form: Annotated[models.LoginForm, fastui_form(models.LoginForm)]) -> list[AnyComponent]:
    user = User(name=form.name, extra={})
    token = user.encode_token()
    return [c.FireEvent(event=AuthEvent(token=token, url='/'))]



@app.get('/{path:path}')
async def html_landing() -> HTMLResponse:
    """Simple HTML page which serves the React app, comes last as it matches all paths."""
    return HTMLResponse(prebuilt_html(title='Reunie Quiz'))


if __name__ == '__main__':
    uvicorn.run('main:app', host='0.0.0.0', port=8000, reload=True)
