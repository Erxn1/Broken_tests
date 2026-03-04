import allure
import pytest
import uuid


@allure.epic("Управление футболками")
@allure.feature("Футболки")
@allure.story("Удаление футболки")
class TestDeleteTshirt:

    @allure.title("Успешное удаление существующей футболки")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.description("""
        Цель: Проверить, что DELETE-запрос удаляет футболку и возвращает 204.
        Шаги:
        1. Создать футболку.
        2. Выполнить DELETE по её ID.
        3. Проверить статус 204.
        4. Попытаться получить футболку по ID – ожидать 404.
        Ожидаемый результат: Футболка удалена, повторный GET даёт 404.
    """)
    def test_delete_existing_tshirt(self, tshirt_client):
        with allure.step("Создание футболки для удаления"):
            dto = {
                "name": "ToDelete",
                "color": "black",
                "size": "M",
                "price": 500,
                "article": f"DEL_{uuid.uuid4().hex[:8]}",
                "material": "cotton",
                "countryOfProduction": "CN",
                "image": "",
                "description": "will be deleted"
            }
            create_resp = tshirt_client.create_tshirt(dto)
            allure.attach(str(create_resp.status_code), name="Статус создания", attachment_type=allure.attachment_type.TEXT)
            allure.attach(create_resp.text, name="Тело ответа создания", attachment_type=allure.attachment_type.JSON)
            assert create_resp.status_code == 201
            tshirt_id = create_resp.json()["id"]
            allure.attach(str(tshirt_id), name="Созданный ID", attachment_type=allure.attachment_type.TEXT)

        with allure.step(f"Выполнение DELETE-запроса для ID {tshirt_id}"):
            del_resp = tshirt_client.delete_tshirt(tshirt_id)
            allure.attach(str(del_resp.status_code), name="HTTP статус удаления", attachment_type=allure.attachment_type.TEXT)
            allure.attach(del_resp.text, name="Тело ответа при удалении", attachment_type=allure.attachment_type.JSON)

        with allure.step("Проверка статуса 204 No Content"):
            assert del_resp.status_code == 204, f"Ожидался 204, получен {del_resp.status_code}"

        with allure.step("Проверка, что футболка действительно удалена (GET -> 404)"):
            get_resp = tshirt_client.get_tshirt_by_id(tshirt_id)
            allure.attach(str(get_resp.status_code), name="HTTP статус GET", attachment_type=allure.attachment_type.TEXT)
            allure.attach(get_resp.text, name="Тело ответа GET", attachment_type=allure.attachment_type.JSON)
            assert get_resp.status_code == 404

    @allure.title("Удаление несуществующей футболки")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.description("""
        Цель: Проверить, что при попытке удалить несуществующую футболку возвращается 404.
        Ожидаемый результат: 404 Not Found.
    """)
    @pytest.mark.parametrize("invalid_id", [
        999999999,
        -1,
        0,
        "string",
        " 9999",
        "@#$",
        "null"
    ])
    def test_delete_nonexistent_tshirt(self, tshirt_client, invalid_id):
        with allure.step(f"Выполнение DELETE-запроса для ID {invalid_id}"):
            del_resp = tshirt_client.delete_tshirt(invalid_id)
            allure.attach(str(del_resp.status_code), name="HTTP статус", attachment_type=allure.attachment_type.TEXT)
            allure.attach(del_resp.text, name="Тело ответа", attachment_type=allure.attachment_type.JSON)

        assert del_resp.status_code == 404, f"Ожидался 404, получен {del_resp.status_code}"
        error = del_resp.json()
        assert "message" in error
        assert "type" in error