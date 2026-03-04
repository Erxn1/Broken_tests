import allure
import pytest


@allure.epic("Управление футболками")
@allure.feature("Футболки")
@allure.story("Получение футболки по ID")
class TestGetTshirtById:

    @allure.title("Успешное получение существующей футболки по ID")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.description("""
        Цель: Проверить, что GET-запрос существующей футболки возвращает 200 и корректные данные.
        Шаги:
        1. Создать футболку через фикстуру.
        2. Выполнить GET по её ID.
        3. Проверить статус 200 и соответствие полей.
        Ожидаемый результат: Данные совпадают с созданными.
    """)
    def test_get_existing_tshirt(self, tshirt_client, created_tshirt):
        tshirt_id = created_tshirt["id"]

        with allure.step(f"Выполнение GET-запроса для ID {tshirt_id}"):
            resp = tshirt_client.get_tshirt_by_id(tshirt_id)
            allure.attach(str(resp.status_code), name="HTTP статус", attachment_type=allure.attachment_type.TEXT)
            allure.attach(resp.text, name="Тело ответа", attachment_type=allure.attachment_type.JSON)

        with allure.step("Проверка статуса 200"):
            assert resp.status_code == 200

        with allure.step("Проверка соответствия данных"):
            data = resp.json()
            assert data["id"] == tshirt_id
            assert data["article"] == created_tshirt["article"]
            assert data["name"] == created_tshirt["name"]
            assert data["color"] == created_tshirt["color"]
            assert data["size"] == created_tshirt["size"]
            assert data["price"] == created_tshirt["price"]

    @allure.title("Получение несуществующей футболки")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.description("""
        Цель: Проверить, что при запросе футболки с несуществующим ID возвращается 404.
        Шаги:
        1. Выполнить GET для ID, который заведомо отсутствует.
        2. Проверить статус 404 и наличие сообщения об ошибке.
        Ожидаемый результат: 404 Not Found.
    """)
    @pytest.mark.parametrize("invalid_id,expected_status", [
        (999999999, 404), #
        (-1, 404), #
        (0, 404), #
        ("string", 400),
        (" 9999", 400),
        ("@#$", 400),
        ("null",400)
    ])
    def test_get_nonexistent_tshirt(self, tshirt_client, invalid_id, expected_status):
        with allure.step(f"Выполнение GET-запроса для ID {invalid_id}"):
            resp = tshirt_client.get_tshirt_by_id(invalid_id)
            allure.attach(str(resp.status_code), name="HTTP статус", attachment_type=allure.attachment_type.TEXT)
            allure.attach(resp.text, name="Тело ответа", attachment_type=allure.attachment_type.JSON)

        assert resp.status_code == expected_status, f"Ожидался {expected_status}, получен {resp.status_code}"
        error = resp.json()
        assert "message" in error
        assert "type" in error