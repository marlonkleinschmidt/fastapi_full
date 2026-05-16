from http import HTTPStatus


def test_root_deve_retornar_ok_e_ola_mundo(client):
    """
    esse teste tem 3 etapas (AAA)
    A - Arrange - arranjo
    A - Act - executa a coisa (o SUT)
    A - Assert - Garanta que A é A
    """
    # Arrange

    # Act
    response = client.get('/')

    # Assert
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'message': 'Olá Mundo!'}


def test_root_deve_retornar_ok_e_ola_mundo_html(client):
    """
    esse teste tem 3 etapas (AAA)
    A - Arrange - arranjo
    A - Act - executa a coisa (o SUT)
    A - Assert - Garanta que A é A
    """
    # Arrange

    # Act
    response = client.get('/h')

    # Assert
    assert response.status_code == HTTPStatus.OK
    assert '<h1> Olá Mundo </h1>' in response.text
