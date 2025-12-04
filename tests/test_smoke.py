from http import HTTPStatus
import allure

@allure.title("Проверить, что приложение запущено")
def test_status_app(status_api_class):
    response = status_api_class.status()
    assert response.status_code == HTTPStatus.OK
    assert response.json()['database'] == True
