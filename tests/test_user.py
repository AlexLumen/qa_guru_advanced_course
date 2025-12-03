from http import HTTPStatus

import allure
import pytest
from app.models.User import User
from tests.clients import get_user


@allure.title("Тест получения пользователя по id")
@pytest.mark.parametrize("user_id", [1, 2, 6, 11, 12])
def test_user(app_url, user_id):
    response = get_user(app_url, user_id)
    assert response.status_code == HTTPStatus.OK
    user = response.json()
    User.model_validate(user)

@allure.title("Проверить возврат ошибки при указании невалидного id")
@pytest.mark.parametrize("user_id", [-1, 0, "fafaf"])
def test_user_invalid_values(app_url, user_id):
    response = get_user(app_url, user_id)
    assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY



@allure.step("Проверить что возвращается 404 при указании несуществующего id")
def test_user_nonexistent_values(app_url,  create_new_user):
    user_id = create_new_user.json()['id'] + 1
    response = get_user(app_url, user_id)
    assert response.status_code == HTTPStatus.NOT_FOUND
