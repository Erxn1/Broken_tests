import allure
import requests

@allure.epic("Тестирование отладочных ручек")
@allure.feature("Flaky endpoint")
@allure.story("Проверка стабильности эндпоинта")
@allure.title("Тест /api/flakyEndpoint ожидает 200 OK")
@allure.description("Этот тест проверяет, что флаковый эндпоинт возвращает 200 при многократных вызовах.")
@allure.severity(allure.severity_level.TRIVIAL)
@allure.tag("flaky")

def test_error_500_flaky(base_url):
    with allure.step("Отправка GET-запроса к /api/flakyEndpoint"):
        response = requests.get(f"{base_url}/api/flakyEndpoint")

    with allure.step("Проверка статус-кода ответа"):
        allure.attach(
            response.text,
            name="Тело ответа",
            attachment_type=allure.attachment_type.TEXT
        )
        assert response.status_code == 200, (
            f"Ждал код 200, получил {response.status_code}"
        )