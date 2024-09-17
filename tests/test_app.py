from http import HTTPStatus

from fast_api_curso.schemas import UserPublic


def test_se_root_retorna_ok_e_mensagem_ola_mundo(client):
    response = client.get('/')
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'message': 'Olá Mundo'}


def test_se_aula02_retorna_ok_e_ola_mundo(client):
    response = client.get('/ex_aula02')
    assert response.status_code == HTTPStatus.OK
    assert 'Olá Mundo!' in response.text


def test_create_user(client):
    response = client.post(
        '/users/',
        json={
            'username': 'Paulo',
            'email': 'teste@teste.com',
            'password': 'senha123',
        },
    )
    assert response.status_code == HTTPStatus.CREATED
    assert response.json() == {
        'username': 'Paulo',
        'email': 'teste@teste.com',
        'id': 1,
    }


def test_exception_create_user_username(client, user):
    response = client.post('/users/',
                           json={
                                 'username': user.username,
                                 'email': 'teste@teste.com',
                                 'password': 'senha123',
        }
   )
    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert response.json() == {'detail': 'Username already exists.'}


def test_exception_create_user_email(client, user):
    response = client.post('/users/',
                           json={
                                 'username': 'José',
                                 'email': user.email,
                                 'password': 'senha123',
        }
   )
    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert response.json() == {'detail': 'E-mail already exists.'}


def test_get_users(client):
    response = client.get('/users/')
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'users': []}


def test_get_users_with_users(client, user):
    user_schema = UserPublic.model_validate(user).model_dump()
    response = client.get('/users/')
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'users': [user_schema]}


def test_get_users_unico(client, user):
    response = client.get('/users/1/')
    assert response.status_code == HTTPStatus.OK

    assert response.json() == {
        'id': 1,
        'username': 'usuario',
        'email': 'teste@teste.com',
    }


def test_exception_get_user_unico(client):
    response = client.get('/users/99')
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'User not found'}


def test_update_user(client, user):
    response = client.put(
        '/users/1',
        json={
            'username': 'Paulo',
            'email': 'teste@test.com',
            'password': '123456789',
        },
    )
    assert response.json() == {
        'id': 1,
        'username': 'Paulo',
        'email': 'teste@test.com',
    }


def test_exception_update_user(client):
    response = client.put(
        '/users/99',
        json={
            'username': 'Paulo',
            'email': 'teste@test.com',
            'password': '123456789',
        },
    )
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'User not found'}


def test_delete_user(client, user):
    response = client.delete('/users/1')
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'message': 'User deleted'}


def test_exception_delete_user(client):
    response = client.delete('/users/99')
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'User not found'}
