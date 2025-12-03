
from http import HTTPStatus

import allure
import pytest

from tests.clients import update_user, get_user
from tests.messages import INVALID_USER_ID





@allure.title("Тест обновления пользователя")
def test_update_user(app_url, create_new_user, user_data_for_edit):
    user_id = create_new_user.json()['id']
    response = update_user(app_url, user_id, user_data_for_edit)
    assert response.status_code == HTTPStatus.OK

    assert response.json()["last_name"] == user_data_for_edit["last_name"]
    assert response.json()["first_name"] == user_data_for_edit["first_name"]
    assert response.json()["email"] == user_data_for_edit["email"]
    assert response.json()["avatar"] == user_data_for_edit["avatar"]

    assert response.json()["last_name"] != create_new_user.json()["last_name"]
    assert response.json()["first_name"] != create_new_user.json()["first_name"]
    assert response.json()["email"] !=create_new_user.json()["email"]
    assert response.json()["avatar"] != create_new_user.json()["avatar"]

    user = get_user(app_url, response.json()['id'])
    assert user.json()["last_name"] == response.json()["last_name"]
    assert user.json()["first_name"] == response.json()["first_name"]
    assert user.json()["email"] == response.json()["email"]
    assert user.json()["avatar"] == response.json()["avatar"]



@allure.title("Тест обновления пользователя  c несуществующим id")
def test_update_user_with_not_exist_id(app_url, create_new_user, user_data_for_edit):
    user_id = create_new_user.json()['id'] + 1
    response = update_user(app_url, user_id, user_data_for_edit)
    assert response.status_code == HTTPStatus.NOT_FOUND



@allure.title("Тест обновления пользователя  c некорректным id")
@pytest.mark.parametrize("user_id", [0, -1, -100])
def test_update_user_with_invalid_id(app_url, create_new_user, user_data_for_edit, user_id):
    response = update_user(app_url, user_id, user_data_for_edit)
    assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY
    assert response.json()["detail"] == INVALID_USER_ID
