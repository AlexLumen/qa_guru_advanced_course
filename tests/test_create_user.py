"""
    Тесты на создание пользователя
"""
from http import HTTPStatus

import allure

from messages.messages import INVALID_FIELD_TYPE_STRING


@allure.title("Создать пользователя")
def test_user_create(users_api_class, user_data):
    response = users_api_class.create_user(user_data)
    assert response.status_code == HTTPStatus.CREATED
    assert "id" in response.json()
    assert response.json()["last_name"] == user_data["last_name"]
    assert response.json()["first_name"] == user_data["first_name"]
    assert response.json()["email"] == user_data["email"]
    assert response.json()["avatar"] == user_data["avatar"]
    user = users_api_class.get_user(response.json()['id'])
    assert user.json()["last_name"] == response.json()["last_name"]
    assert user.json()["first_name"] == response.json()["first_name"]
    assert user.json()["email"] == response.json()["email"]
    assert user.json()["avatar"] == response.json()["avatar"]




@allure.title("Создать пользователя  без email")
def test_user_create_without_email(users_api_class, user_data):
    user_data['email'] = None
    response = users_api_class.create_user(user_data)
    assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY
    assert response.json()["detail"][0]['msg'] == INVALID_FIELD_TYPE_STRING

@allure.title("Создать пользователя  без first_name")
def test_user_create_without_first_name(users_api_class, user_data):
    user_data['first_name'] = None
    response = users_api_class.create_user(user_data)
    assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY
    assert response.json()["detail"][0]['msg'] == INVALID_FIELD_TYPE_STRING


@allure.title("Создать пользователя  без last_name")
def test_user_create_without_last_name(users_api_class, user_data):
    user_data['last_name'] = None
    response = users_api_class.create_user(user_data)
    assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY
    assert response.json()["detail"][0]['msg'] == INVALID_FIELD_TYPE_STRING


@allure.title("Создать пользователя  без avatar")
def test_user_create_without_avatar(users_api_class,user_data):
    user_data['avatar'] = None
    response = users_api_class.create_user(user_data)
    assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY
    assert response.json()["detail"][0]['msg'] == INVALID_FIELD_TYPE_STRING
