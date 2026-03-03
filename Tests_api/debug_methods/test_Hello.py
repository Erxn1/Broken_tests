import allure
import requests

@allure.epic("Тестирование отладочных ручек")
@allure.feature("Hello endpoint")
@allure.story("Приветственное сообщение")
@allure.title("Тест /api/hello ожидает 200 OK и приветствие 'Hello, Stasyan'")
@allure.description("Проверяем, что ручка /api/hello возвращает корректный статус и содержит ожидаемое сообщение.")
@allure.severity(allure.severity_level.TRIVIAL)

def test_hello(base_url):
    with allure.step("Отправка GET-запроса к /api/hello"):
        response = requests.get(f"{base_url}/api/hello")
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

    with allure.step("Проверка наличия приветствия 'Hello, Stasyan'"):
        assert "Hello, Stasyan" in response.text, (
            f"Ожидаю сообщение 'Hello, Stasyan', но получил: {response.text}"
        )