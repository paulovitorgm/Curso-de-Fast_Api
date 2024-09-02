from http import HTTPStatus

from fastapi import FastAPI
from fastapi.responses import HTMLResponse

from fast_api_curso.schemas import Message

app = FastAPI()


@app.get("/", status_code=HTTPStatus.OK, response_model=Message)
def root():
    return {"message": "Olá Mundo", "teste": "mensagem"}


@app.get("/ex_aula02", status_code=HTTPStatus.OK, response_class=HTMLResponse)
def aula02():
    return """  <!DOCTYPE html>
            <html lang="pt-br">
                <head>
                    <meta charset="UTF-8">
                    <title>Title</title>
                </head>
                <body>
                    <h1>Olá Mundo!</h1>
                </body>
            </html>"""
