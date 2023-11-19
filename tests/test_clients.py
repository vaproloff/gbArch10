import pytest
from fastapi.testclient import TestClient
from main import app


# Тест для эндпоинта получения всех клиентов
def test_get_all_clients(temp_db):
    with TestClient(app) as client:
        response = client.get("/clients/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
    assert response.json() == []


# Тест создания клиента
def test_create_client(temp_db):
    client_data = {
        "document": "1234567890",
        "surname": "Иванов",
        "first_name": "Иван",
        "patronymic": "Иванович",
        "birthday": "1990-01-01",
    }
    with TestClient(app) as client:
        response = client.post("/clients/", json=client_data)
    assert response.status_code == 200
    assert "id" in response.json()

    # Проверим, что клиент действительно создан
    with TestClient(app) as client:
        response = client.get(f"/clients/{response.json()['id']}")
    assert response.status_code == 200
    assert response.json() == {**client_data, "id": response.json()["id"]}


# Тест валидации документа при создании клиента
def test_doc_validating(temp_db):
    client_data = {
        "document": "1234",
        "surname": "Иванов",
        "first_name": "Иван",
        "patronymic": "Иванович",
        "birthday": "1990-01-01",
    }
    with TestClient(app) as client:
        response = client.post("/clients/", json=client_data)
    assert response.status_code == 422
    assert response.json()['detail'][0]['msg'] == 'String should have at least 10 characters'


# Тест валидации даты рождения при создании клиента
def test_birthday_validating(temp_db):
    client_data = {
        "document": "1234567890",
        "surname": "Иванов",
        "first_name": "Иван",
        "patronymic": "Иванович",
        "birthday": "2010-01-01",
    }
    with TestClient(app) as client:
        response = client.post("/clients/", json=client_data)
    assert response.status_code == 422
    assert response.json()['detail'][0]['msg'] == 'Value error, Age must be between 18 and 100.'


# Тест обновления клиента
def test_update_client(temp_db):
    # Создадим клиента для обновления
    client_data = {
        "document": "1234567890",
        "surname": "Иванов",
        "first_name": "Иван",
        "patronymic": "Иванович",
        "birthday": "1990-01-01",
    }
    with TestClient(app) as client:
        response = client.post("/clients/", json=client_data)
    assert response.status_code == 200
    client_id = response.json()["id"]

    # Обновим данные клиента
    new_client_data = {
        "document": "0987654321",
        "surname": "Петров",
        "first_name": "Петр",
        "patronymic": "Петрович",
        "birthday": "1980-01-01",
    }
    with TestClient(app) as client:
        response = client.put(f"/clients/{client_id}", json=new_client_data)
    assert response.status_code == 200
    assert response.json() == {**new_client_data, "id": client_id}


# Тест удаления клиента
def test_delete_client(temp_db):
    # Создадим клиента для удаления
    client_data = {
        "document": "1234567890",
        "surname": "Иванов",
        "first_name": "Иван",
        "patronymic": "Иванович",
        "birthday": "1990-01-01",
    }
    with TestClient(app) as client:
        response = client.post("/clients/", json=client_data)
    assert response.status_code == 200
    client_id = response.json()["id"]

    # Удалим клиента
    with TestClient(app) as client:
        response = client.delete(f"/clients/{client_id}")
    assert response.status_code == 200
    assert response.json() == {"message": "User deleted"}

    # Проверим, что клиента больше нет
    with TestClient(app) as client:
        response = client.get(f"/clients/{client_id}")
    assert response.status_code == 404


if __name__ == '__main__':
    pytest.main(['-v'])
