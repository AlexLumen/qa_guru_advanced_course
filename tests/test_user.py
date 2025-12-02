from http import HTTPStatus

import allure
import pytest
from app.models.User import User


@allure.title("Тест получения пользователя по id")
@pytest.mark.parametrize("user_id", [1, 2, 6, 11, 12])
def test_user(users_api_class, user_id):
    response = users_api_class.get_user(user_id)
    assert response.status_code == HTTPStatus.OK
    user = response.json()
    User.model_validate(user)

@allure.title("Проверить возврат ошибки при указании невалидного id")
@pytest.mark.parametrize("user_id", [-1, 0, "fafaf"])
def test_user_invalid_values(users_api_class, user_id):
    response = users_api_class.get_user(user_id)
    assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY



@allure.step("Проверить что возвращается 404 при указании несуществующего id")
def test_user_nonexistent_values(users_api_class,  create_new_user):
    user_id = create_new_user.json()['id'] + 1
    response = users_api_class.get_user( user_id)
    assert response.status_code == HTTPStatus.NOT_FOUND
