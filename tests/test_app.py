from http import HTTPStatus


def test_se_root_retorna_ok_e_mensagem_ola_mundo(client):
    # Act - Ação
    response = client.get('/')
    # Assert  - Afirmação
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


def test_get_users(client):
    response = client.get("/users/")
    assert response.status_code == HTTPStatus.OK

    assert response.json() == {
        'users': [
            {
                'id': 1,
                'username': 'Paulo',
                'email': 'teste@teste.com',
            }
        ]
    }


def test_get_users_unico(client):
    response = client.get("/users/1/")
    assert response.status_code == HTTPStatus.OK

    assert response.json() == {
                'id': 1,
                'username': 'Paulo',
                'email': 'teste@teste.com',
            }


def test_exception_get_user_unico(client):
    response = client.get('/users/99')
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'User not found'}


def test_update_user(client):
    response = client.put(
        '/users/1',
        json={
            'username': 'Paulo',
            'email': 'teste@test.com',
            'password': '123456789'}
    )
    assert response.json() == {
        'id': 1,
        'username': 'Paulo',
        'email': 'teste@test.com'
        }


def test_exception_update_user(client):
    response = client.put(
        '/users/99',
        json={
            'username': 'Paulo',
            'email': 'teste@test.com',
            'password': '123456789'}
    )
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {
            'detail': 'User not found'
    }


def test_delete_user(client):
    response = client.delete('/users/1')
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'message': 'User deleted'}


def test_exception_delete_user(client):
    response = client.delete('/users/99')
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'User not found'}
