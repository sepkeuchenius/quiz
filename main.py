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
from fastui.events import GoToEvent, BackEvent
from pydantic import BaseModel, Field

import uvicorn
import questions


app = FastAPI()

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
def index() -> list[AnyComponent]:
    """
    User profile page, the frontend will fetch this when the user visits `/user/{id}/`.
    """ 
    return page(c.ModelForm(model=models.User, submit_url='/question/0', method='GOTO'), title="Reunie Quiz - Home")

@app.get("/api/start", response_model=FastUI, response_model_exclude_none=True)
def quiz(name: str) -> list[AnyComponent]:
    """
    User profile page, the frontend will fetch this when the user visits `/user/{id}/`.
    """ 
    return page(c.Heading(text=f'Alright {name}. Lets go!'), c.ModelForm(model=models.QuestionForm, submit_url=f"/next/{0}", method="GOTO"), title='Quiz')


@app.get("/api/question/{index}", response_model=FastUI, response_model_exclude_none=True)
def quiz(answer: str, index: str) -> list[AnyComponent]:
    """
    User profile page, the frontend will fetch this when the user visits `/user/{id}/`.
    """ 
    q=questions.get_question(int(index), answer)
    if q is not None:
        return page(*q, c.ModelForm(model=models.QuestionForm, submit_url=f"/question/{int(index)+1}", method='GOTO'), title='Quiz')
    else:
        return page(c.Text(text="Dat was m alweer!"), title='Quiz Klaar!')



@app.get('/{path:path}')
async def html_landing() -> HTMLResponse:
    """Simple HTML page which serves the React app, comes last as it matches all paths."""
    return HTMLResponse(prebuilt_html(title='Reunie Quiz'))


if __name__ == '__main__':
    uvicorn.run('main:app', host='0.0.0.0', port=8000, reload=True)
