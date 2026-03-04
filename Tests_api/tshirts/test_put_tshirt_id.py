import allure
import pytest
import uuid


@allure.epic("Управление футболками")
@allure.feature("Футболки")
@allure.story("Редактирование футболки")
class TestUpdateTshirt:

    @staticmethod
    def _unique_article(prefix="PUT"):
        return f"{prefix}_{uuid.uuid4().hex[:8]}"

    @allure.title("Успешное обновление всех полей футболки")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.description("""
        Цель: Проверить, что PUT-запрос с корректными данными обновляет все поля футболки.
        Шаги:
        1. Создать футболку через фикстуру.
        2. Отправить PUT-запрос с новыми значениями всех полей.
        3. Проверить статус 200 и соответствие обновлённых данных.
        4. Получить футболку по ID и убедиться, что изменения применились.
        Ожидаемый результат: Все поля обновлены, сервер возвращает обновлённый объект.
    """)
    def test_update_all_fields(self, tshirt_client, created_tshirt):
        tshirt_id = created_tshirt["id"]
        new_dto = {
            "article": self._unique_article("UPD"),
            "name": "Обновлённая футболка",
            "size": "XL",
            "color": "black",
            "image": "new_image",
            "material": "silk",
            "countryOfProduction": "Italy",
            "description": "новое описание",
            "price": 2500.0
        }

        with allure.step("Отправка PUT-запроса на обновление"):
            resp = tshirt_client.update_tshirt(tshirt_id, new_dto)
            allure.attach(str(resp.status_code), name="HTTP статус", attachment_type=allure.attachment_type.TEXT)
            allure.attach(resp.text, name="Тело ответа", attachment_type=allure.attachment_type.JSON)

        with allure.step("Проверка статуса 200"):
            assert resp.status_code == 200

        with allure.step("Проверка, что ответ содержит обновлённые данные"):
            updated = resp.json()
            assert updated["id"] == tshirt_id
            for key, value in new_dto.items():
                assert updated[key] == value, f"Поле {key} не совпадает: ожидалось {value}, получено {updated[key]}"

        with allure.step("Проверка через GET-запрос, что данные действительно обновлены"):
            get_resp = tshirt_client.get_tshirt_by_id(tshirt_id)
            assert get_resp.status_code == 200
            get_data = get_resp.json()
            for key, value in new_dto.items():
                assert get_data[key] == value

    @allure.title("Обновление с минимально допустимыми значениями")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.description("""
        Цель: Проверить обновление с минимальными значениями обязательных полей (например, цена 0, пустые строки для необязательных).
        Ожидаемый результат: 200 OK, данные обновлены.
    """)
    def test_update_minimal_values(self, tshirt_client, created_tshirt):
        tshirt_id = created_tshirt["id"]
        new_dto = {
            "article": self._unique_article("MIN"),
            "name": "A",  # минимальная длина
            "size": "XS",
            "color": "white",
            "material": "wool",
            "countryOfProduction": "FR",
            "price": 0.0,
            "image": "",      # пустая строка допустима
            "description": "" # пустая строка допустима
        }

        resp = tshirt_client.update_tshirt(tshirt_id, new_dto)
        assert resp.status_code == 200
        updated = resp.json()
        assert updated["price"] == 0.0
        assert updated["image"] == ""
        assert updated["description"] == ""

    @allure.title("Попытка обновить несуществующую футболку")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.description("""
        Цель: Проверить, что при попытке обновить футболку с несуществующим ID возвращается 404.
    """)
    def test_update_not_found(self, tshirt_client):
        non_existent_id = 999999999
        dto = {
            "article": "NONEXIST",
            "name": "Test",
            "size": "M",
            "color": "red",
            "material": "cotton",
            "countryOfProduction": "CN",
            "price": 100
        }
        resp = tshirt_client.update_tshirt(non_existent_id, dto)
        assert resp.status_code == 404
        error = resp.json()
        assert "message" in error
        assert "type" in error

    # ---------- Негативные сценарии ----------
    @allure.title("Обновление с отсутствующим обязательным полем: {missing_field}")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.parametrize("missing_field", [
        "article", "name", "size", "color", "material", "countryOfProduction", "price"
    ])
    def test_update_missing_required_field(self, tshirt_client, created_tshirt, missing_field):
        tshirt_id = created_tshirt["id"]
        dto = {
            "article": self._unique_article("MISS"),
            "name": "Valid Name",
            "size": "L",
            "color": "red",
            "material": "cotton",
            "countryOfProduction": "CN",
            "price": 100,
            "image": "",
            "description": ""
        }
        del dto[missing_field]

        resp = tshirt_client.update_tshirt(tshirt_id, dto)
        assert resp.status_code == 400
        error = resp.json()
        assert "message" in error

    @allure.title("Обновление с невалидными типами данных")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.parametrize("field,value,expected_status", [
        ("price", "сто рублей", 400),   # строка вместо числа
        ("price", -10, 400),             # отрицательная цена (минимальное 0)
        ("price", 1.5, 200),             # дробное число допустимо
        ("size", 123, 200),              # число преобразуется в строку
        ("color", "", 200),               # пустая строка допустима
    ])
    def test_update_invalid_types(self, tshirt_client, created_tshirt, field, value, expected_status):
        tshirt_id = created_tshirt["id"]
        dto = {
            "article": self._unique_article("TYPE"),
            "name": "Test",
            "size": "L",
            "color": "red",
            "material": "cotton",
            "countryOfProduction": "CN",
            "price": 100,
            "image": "",
            "description": ""
        }
        dto[field] = value

        resp = tshirt_client.update_tshirt(tshirt_id, dto)
        assert resp.status_code == expected_status
        if expected_status == 400:
            error = resp.json()
            assert "message" in error
        else:
            updated = resp.json()
            assert updated[field] == str(value) if isinstance(value, int) and field == "size" else updated[field] == value

    @allure.title("Обновление с полями, превышающими максимальную длину")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.parametrize("field", ["name", "color", "size", "material", "countryOfProduction", "description", "article"])
    def test_update_field_too_long(self, tshirt_client, created_tshirt, field):
        tshirt_id = created_tshirt["id"]
        dto = {
            "article": self._unique_article("LONG"),
            "name": "Test",
            "size": "L",
            "color": "red",
            "material": "cotton",
            "countryOfProduction": "CN",
            "price": 100,
            "image": "",
            "description": ""
        }
        long_value = "a" * 256
        dto[field] = long_value

        resp = tshirt_client.update_tshirt(tshirt_id, dto)
        if resp.status_code == 400:
            error = resp.json()
            assert "message" in error
        else:
            assert resp.status_code == 200
            updated = resp.json()
            assert len(updated[field]) <= 255