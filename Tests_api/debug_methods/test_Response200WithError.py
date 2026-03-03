import allure
import requests

@allure.epic("Тестирование отладочных ручек")
@allure.feature("Response200WithError endpoint")
@allure.story("Проверка ответа с кодом 200 и текстом ошибки")
@allure.title("Тест /api/response200WithError ожидает 200 и сообщение 'Error: Я не смогла'")
@allure.description("Ручка возвращает 200 OK, но в теле передаёт сообщение об ошибке. Проверяем корректность.")
@allure.severity(allure.severity_level.TRIVIAL)

def test_response200_with_error(base_url):
    with allure.step("Отправка GET-запроса к /api/response200WithError"):
        response = requests.get(f"{base_url}/api/response200WithError")
        allure.attach(
            response.text,
            name="Тело ответа",
            attachment_type=allure.attachment_type.TEXT
        )

    with allure.step("Проверка статус-кода ответа"):
        assert response.status_code == 200, (
            f"Ожидаю статус код 200, но получил: {response.status_code}"
        )

    with allure.step("Проверка, что тело ответа не пустое"):
        assert response.text, "Тело ответа пустое"

    with allure.step("Проверка наличия сообщения об ошибке"):
        assert "Error: Я не смогла" in response.text, (
            f"В ответе нет ожидаемого сообщения 'Error: Я не смогла'. Фактический ответ: {response.text}"
        )