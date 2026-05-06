from http import HTTPStatus

from fastapi.testclient import TestClient

from fastapi_full.app import app


def test_root_deve_retornar_ok_e_ola_mundo():
    """
    esse teste tem 3 etapas (AAA)
    A - Arrange - arranjo
    A - Act - executa a coisa (o SUT)
    A - Assert - Garanta que A é A
    """
    # Arrange
    client = TestClient(app)
    # Act
    response = client.get('/')

    # Assert
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'message': 'Olá Mundo!'}
