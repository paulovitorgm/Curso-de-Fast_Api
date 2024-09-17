from http import HTTPStatus

from fastapi import Depends, FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from sqlalchemy import select
from sqlalchemy.orm import Session

from fast_api_curso.database import get_session
from fast_api_curso.models import User
from fast_api_curso.schemas import (
    Message,
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
def create_users(user: UserSchema, session=Depends(get_session)):
    # Caso não encontre no banco de dados nenhum usuario ou email
    # já existente igual ao passado retornará None
    db_user = session.scalar(
        select(User).where(
            (User.username == user.username) or (User.email == user.email)
        )
    )

    if db_user:
        if db_user.username == user.username:
            raise HTTPException(
                status_code=HTTPStatus.BAD_REQUEST,
                detail='Username already exists.',
            )
        elif db_user.email == user.email:
            raise HTTPException(
                status_code=HTTPStatus.BAD_REQUEST,
                detail='E-mail already exists.',
            )

    db_user = User(
        username=user.username, password=user.password, email=user.email
    )

    session.add(db_user)
    session.commit()
    session.refresh(db_user)

    return db_user


@app.get('/users/', response_model=UserList)
def read_users(
    session: Session = Depends(get_session), limit: int = 10, skip: int = 0
):
    users = session.scalars(select(User).offset(skip).limit(limit)).all()
    return {'users': users}


@app.get(
    '/users/{user_id}', status_code=HTTPStatus.OK, response_model=UserPublic
)
def read_users_solo(user_id: int, session: Session = Depends(get_session)):
    db_user = session.scalar(select(User).where(User.id == user_id))
    if not db_user:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail='User not found'
        )

    return db_user


@app.put('/users/{user_id}', response_model=UserPublic)
def update_user(user_id: int, user: UserSchema,
                session: Session = Depends(get_session)):
    db_user = session.scalar(select(User).where(User.id == user_id))
    if not db_user:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND,
                            detail='User not found')
    db_user.username = user.username
    db_user.password = user.password
    db_user.email = user.email

    session.add(db_user)
    session.commit()
    return db_user


@app.delete(
    '/users/{user_id}', response_model=Message, status_code=HTTPStatus.OK
)
def delete_user(user_id: int, session: Session = Depends(get_session)):
    db_user = session.scalar(select(User).where(User.id == user_id))
    if not db_user:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND,
                            detail='User not found')
    session.delete(db_user)
    session.commit()

    return {'message': 'User deleted'}
