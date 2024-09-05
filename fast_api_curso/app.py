from http import HTTPStatus

from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse

from fast_api_curso.schemas import (
    Message,
    UserDB,
    UserList,
    UserPublic,
    UserSchema,
)

app = FastAPI()

database = []


@app.get('/', status_code=HTTPStatus.OK, response_model=Message)
def root():
    return {'message': 'Olá Mundo'}


@app.get('/ex_aula02', status_code=HTTPStatus.OK, response_class=HTMLResponse)
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


@app.post('/users/', status_code=HTTPStatus.CREATED, response_model=UserPublic)
def create_users(user: UserSchema):
    user_with_id = UserDB(id=len(database) + 1, **user.model_dump())
    database.append(user_with_id)
    return user_with_id


@app.get('/users/', status_code=HTTPStatus.OK, response_model=UserList)
def read_users():
    return {'users': database}


@app.get('/users/{user_id}', status_code=HTTPStatus.OK,
         response_model=UserPublic)
def read_users_solo(user_id: int):
    if user_id < 1 or user_id > len(database) + 1:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND,
                            detail='User not found')

    user_with_id = database[user_id - 1]
    return user_with_id


@app.put('/users/{user_id}', response_model=UserPublic)
def update_user(user_id: int, user: UserSchema):
    if user_id < 1 or user_id > len(database) + 1:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND,
                            detail='User not found')
    user_with_id = UserDB(id=user_id, **user.model_dump())
    database[user_id - 1] = user_with_id
    return user_with_id


@app.delete('/users/{user_id}', response_model=Message,
            status_code=HTTPStatus.OK)
def delete_user(user_id: int):
    if user_id < 1 or user_id > len(database) + 1:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND,
                            detail='User not found')

    del database[user_id - 1]
    return {'message': 'User deleted'}
