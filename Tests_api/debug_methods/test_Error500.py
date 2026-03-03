import requests
import allure

@allure.epic("Тестирование отладочных ручек")
@allure.feature("Error500 endpoint")
@allure.story("Проверка стабильности эндпоинта")
@allure.title("Тест /api/error500 ожидает код 500 ")
@allure.description("Этот тест проверяет, что ручка возвращает код 500")
@allure.severity(allure.severity_level.TRIVIAL)

def test_error_500(base_url):
    with allure.step("Отправка GET запроса к /api/error500"):
        response=requests.get(f"{base_url}/api/error500")

    with allure.step("Проверка статус-кода ответа"):
        assert response.status_code == 500, (
        f"Ждал код 500 получил :{response.status_code}"
        )

    with allure.step("Проверка что теле ответа есть сообщение об ошибке: 'Статус кода: 500'"):
        assert response.text == "Статус кода: 500", (
            f"Ждал сообщение : 'Статус кода: 500', но получил {response.text}"
        )

