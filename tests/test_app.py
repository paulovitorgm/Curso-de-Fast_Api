from http import HTTPStatus

from fastapi.testclient import TestClient

from fast_api_curso.app import app


def test_se_root_retorna_ok_e_mensagem_ola_mundo():
    # Arrange - Organização
    client = TestClient(app)

    # Act - Ação
    response = client.get("/")

    # Assert  - Afirmação
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {"message": "Olá Mundo"}


def test_se_aula02_retorna_ok_e_ola_mundo():
    client = TestClient(app)
    response = client.get("/ex_aula02")
    assert response.status_code == HTTPStatus.OK
    assert "Olá Mundo!" in response.text
