import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)




@pytest.fixture(scope='module')
def auth_token():
    response = client.post(
        "/token",  
        data={"username": "tiziano", "password": "secret"}  
    )
    assert response.status_code == 200
    return response.json()["access_token"]

#-----------------------------------------------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------------------------------------------


def test_create_user(auth_token):
    response = client.post("/usuarios/crear",
        json={"id": 12, "username": "username", "email": "email@example.com", "created_at": "2000-01-01"},
        headers={"Authorization": f"Bearer {auth_token}"}
    )
    assert response.status_code == 200
    assert response.json() == {"message": "Usuario creado"}


# #-----------------------------------------------------------------------------------------------------------------------

def test_leer_user(auth_token):
    response = client.get("/usuarios/leer",
        headers={"Authorization": f"Bearer {auth_token}"}
    )
    assert response.status_code == 200
    users = response.json()
    assert len(users) == 1  # Esperamos obtener una lista con un solo usuario
    user = users[0]
    assert user["username"] == "username"
    assert user["email"] == "email@example.com"
    assert user["created_at"] == "2000-01-01T00:00:00"

#-----------------------------------------------------------------------------------------------------------------------


def test_actualizar_user(auth_token):
    response = client.put("/usuarios/actualizar/2",
        json={"id": 12, "username": "new_username", "email": "new_email@example.com", "created_at": "2022-01-01"},
        headers={"Authorization": f"Bearer {auth_token}"}
    )
    assert response.status_code == 200

    # Verificar que el usuario se haya actualizado correctamente
    assert response.json() == {"message": "Usuario actualizado"}

#-----------------------------------------------------------------------------------------------------------------------

def test_desactualizar_user(auth_token):

    # Actualizar el usuario
    response = client.put("/usuarios/actualizar/2",
        json={"id": 12, "username": "username", "email": "email@example.com", "created_at": "2000-01-01"},
        headers={"Authorization": f"Bearer {auth_token}"}
    )
    assert response.status_code == 200

    # Verificar que el usuario se haya actualizado correctamente
    assert response.json() == {"message": "Usuario actualizado"}


def test_borrar(auth_token):
    response = client.delete("/usuarios/borrar-todos",
        headers={"Authorization": f"Bearer {auth_token}"}
    )
    assert response.status_code == 200
    assert "message" in response.json()
    assert "Se eliminaron" in response.json()["message"]



# para especificar que test hacer es pytest test_main.py::test_leer_user --- pytest nombre-archivo::nombre-funcion
