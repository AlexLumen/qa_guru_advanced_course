from http import HTTPStatus
import allure
from tests.clients import status


@allure.title("Проверить, что приложение запущено")
def test_status_app(app_url):
    response = status(app_url)
    assert response.status_code == HTTPStatus.OK
    assert response.json()['database'] == True
