import uuid
import allure
import pytest


@allure.epic("Управление футболками")
@allure.feature("Футболки")
class TestTshirts:

    @staticmethod
    def _unique_article(prefix="ART"):
        return f"{prefix}_{uuid.uuid4().hex[:8]}"

    @allure.story("Создание футболки")
    @allure.title("Успешное создание футболки без картинки")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.description("""
        Цель: Проверить, что футболка успешно создаётся без изображения.

        Шаги:
        1. Отправить POST-запрос на /t-shirt с корректными данными (все поля заполнены).
        2. Проверить, что статус ответа = 201.
        3. Извлечь ID созданной футболки из ответа.
        4. Выполнить GET-запрос по этому ID для проверки, что данные совпадают с отправленными.
        5. Удалить созданную футболку.

        Ожидаемый результат: Футболка создаётся, возвращается ID, данные соответствуют отправленным.
    """)
    def test_create_tshirt_success(self, tshirt_client):
        with allure.step("Подготовка данных для создания футболки"):
            dto = {
                "name": "Тестовая футболка",
                "color": "red",
                "size": "L",
                "price": 1500,
                "article": self._unique_article("TS-001"),
                "material": "Хлопок",
                "countryOfProduction": "Россия",
                "description": "Описание",
                "image": ""
            }

        with allure.step("Отправка POST-запроса для создания футболки"):
            resp = tshirt_client.create_tshirt(dto)
            allure.attach(str(resp.status_code), name="HTTP статус", attachment_type=allure.attachment_type.TEXT)
            allure.attach(resp.text, name="Тело ответа", attachment_type=allure.attachment_type.JSON)

        with allure.step("Проверка статуса ответа = 201"):
            assert resp.status_code == 201

        data = resp.json()
        with allure.step("Проверка наличия ID в ответе"):
            assert "id" in data, "Ответ не содержит ID созданной футболки"

        with allure.step("Проверка созданной футболки через GET-запрос"):
            get_resp = tshirt_client.get_tshirt_by_id(data["id"])
            allure.attach(str(get_resp.status_code), name="HTTP статус GET",
                          attachment_type=allure.attachment_type.TEXT)
            allure.attach(get_resp.text, name="Тело ответа GET", attachment_type=allure.attachment_type.JSON)
            assert get_resp.status_code == 200
            created = get_resp.json()
            assert created["name"] == dto["name"]
            assert created["color"] == dto["color"]

        with allure.step("Удаление созданной футболки"):
            del_resp = tshirt_client.delete_tshirt(data["id"])
            assert del_resp.status_code in (200, 204)

    @allure.story("Создание футболки")
    @allure.title("Успешное создание футболки с картинкой")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.description("""
        Цель: Проверить, что футболка успешно создаётся с прикреплённым файлом изображения.

        Шаги:
        1. Отправить POST-запрос на /t-shirt с корректными данными и файлом test.jpg.
        2. Проверить статус 201 и наличие ID.
        3. Удалить созданную футболку.

        Ожидаемый результат: Футболка создаётся, файл принимается.
    """)
    def test_create_tshirt_with_picture(self, tshirt_client, test_picture_path):
        with allure.step("Подготовка данных для создания футболки"):
            dto = {
                "name": "Футболка с картинкой",
                "color": "blue",
                "size": "M",
                "price": 2000,
                "article": self._unique_article("TS-002"),
                "material": "Полиэстер",
                "countryOfProduction": "Китай",
                "description": "С картинкой",
                "image": ""
            }

        with allure.step("Отправка POST-запроса с файлом изображения"):
            resp = tshirt_client.create_tshirt(dto, picture_path=test_picture_path)
            allure.attach(str(resp.status_code), name="HTTP статус", attachment_type=allure.attachment_type.TEXT)
            allure.attach(resp.text, name="Тело ответа", attachment_type=allure.attachment_type.JSON)

        with allure.step("Проверка статуса ответа = 201"):
            assert resp.status_code == 201

        data = resp.json()
        with allure.step("Проверка наличия ID в ответе"):
            assert "id" in data

        with allure.step("Удаление созданной футболки"):
            tshirt_client.delete_tshirt(data["id"])

    @allure.story("Создание футболки")
    @allure.title("Успешное создание футболки со всеми обязательными полями")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.description("""
        Цель: Проверить, что футболка создаётся, если указаны только обязательные поля.
        Обязательные поля: name, color, size, price, article, material, countryOfProduction.

        Шаги:
        1. Отправить POST-запрос с минимальным набором полей.
        2. Проверить статус 201 и наличие ID.
        3. Удалить созданную футболку.

        Ожидаемый результат: Футболка успешно создаётся.
    """)
    def test_create_tshirt_all_required_fields(self, tshirt_client):
        with allure.step("Подготовка данных с обязательными полями"):
            dto = {
                "name": "Все обязательные",
                "color": "green",
                "size": "S",
                "price": 500,
                "article": self._unique_article("REQ"),
                "material": "Лен",
                "countryOfProduction": "Индия",
                "image": ""
            }

        with allure.step("Отправка POST-запроса"):
            resp = tshirt_client.create_tshirt(dto)
            allure.attach(str(resp.status_code), name="HTTP статус", attachment_type=allure.attachment_type.TEXT)
            allure.attach(resp.text, name="Тело ответа", attachment_type=allure.attachment_type.JSON)

        with allure.step("Проверка статуса ответа = 201"):
            assert resp.status_code == 201

        data = resp.json()
        with allure.step("Проверка наличия ID в ответе"):
            assert "id" in data

        with allure.step("Удаление созданной футболки"):
            tshirt_client.delete_tshirt(data["id"])

    # ---------- Негативные сценарии ----------
    @allure.story("Негативные сценарии")
    @allure.title("Создание футболки без обязательного поля: {missing_field}")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.description("""
        Цель: Проверить, что при отсутствии обязательного поля сервер возвращает ошибку 400.

        Шаги:
        1. Сформировать полный набор данных, затем удалить одно поле.
        2. Отправить POST-запрос.
        3. Проверить статус 400 и наличие сообщения об ошибке.

        Ожидаемый результат: Ошибка валидации с кодом 400.
    """)
    @pytest.mark.parametrize("missing_field", [
        "name", "color", "size", "price", "article", "material", "countryOfProduction"
    ])
    def test_create_tshirt_missing_field(self, tshirt_client, missing_field):
        with allure.step(f"Подготовка данных без поля: {missing_field}"):
            dto = {
                "name": "Valid Name",
                "color": "red",
                "size": "L",
                "price": 1000,
                "article": self._unique_article("MISS"),
                "material": "cotton",
                "countryOfProduction": "China",
                "description": "some desc",
                "image": ""
            }
            del dto[missing_field]

        with allure.step("Отправка POST-запроса"):
            resp = tshirt_client.create_tshirt(dto)
            allure.attach(str(resp.status_code), name="HTTP статус", attachment_type=allure.attachment_type.TEXT)
            allure.attach(resp.text, name="Тело ответа", attachment_type=allure.attachment_type.JSON)

        with allure.step("Проверка статуса ответа = 400"):
            assert resp.status_code == 400

        with allure.step("Проверка наличия сообщения об ошибке"):
            error = resp.json()
            assert "message" in error
            assert "type" in error

    @allure.story("Негативные сценарии")
    @allure.title("Создание футболки с невалидными типами данных: поле {field} = {value}")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.description("""
        Цель: Проверить обработку неверных типов данных.
        Для каждого кейса указан ожидаемый статус (400 или 201) в зависимости от того,
        допускает ли API преобразование типа.

        Ожидаемый результат: Соответствие ожидаемому статусу и, при ошибке, наличие сообщения.
    """)
    @pytest.mark.parametrize("field,value,expected_status", [
        ("price", "сто рублей", 400),  # строка вместо числа -> ошибка
        ("price", -100, 400),  # отрицательная цена -> ошибка
        ("price", 1.5, 201),  # число с плавающей точкой — валидно
        ("size", 123, 201),  # число преобразуется в строку — валидно
        ("color", "", 201),  # пустая строка допустима — валидно
    ])
    def test_create_tshirt_invalid_types(self, tshirt_client, field, value, expected_status):
        with allure.step(f"Подготовка данных: поле {field} = {value} (тип {type(value).__name__})"):
            dto = {
                "name": "Test",
                "color": "red",
                "size": "L",
                "price": 1000,
                "article": self._unique_article("TYPE"),
                "material": "cotton",
                "countryOfProduction": "China",
                "description": "desc",
                "image": ""
            }
            dto[field] = value

        with allure.step("Отправка POST-запроса"):
            resp = tshirt_client.create_tshirt(dto)
            allure.attach(str(resp.status_code), name="HTTP статус", attachment_type=allure.attachment_type.TEXT)
            allure.attach(resp.text, name="Тело ответа", attachment_type=allure.attachment_type.JSON)

        with allure.step(f"Проверка статуса ответа = {expected_status}"):
            assert resp.status_code == expected_status, f"Ожидался {expected_status}, получен {resp.status_code}"

        if expected_status == 400:
            with allure.step("Проверка наличия сообщения об ошибке"):
                error = resp.json()
                assert "message" in error
        else:
            with allure.step("Проверка наличия ID созданной футболки и очистка"):
                data = resp.json()
                assert "id" in data
                tshirt_client.delete_tshirt(data["id"])

    @allure.story("Негативные сценарии")
    @allure.title("Создание футболки с полем {field} длиной 256 символов (превышение)")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.description("""
        Цель: Проверить поведение API при превышении максимальной длины поля (предположительно 255 символов).
        В зависимости от реализации сервер может вернуть 400 (ошибка валидации) или 201 (обрезав поле).

        Шаги:
        1. Сформировать данные, где указанное поле содержит 256 символов 'a'.
        2. Отправить POST-запрос.
        3. В зависимости от ответа проверить ошибку или успешное создание.
    """)
    @pytest.mark.parametrize("field", ["name", "color", "size", "material", "countryOfProduction", "description"])
    def test_create_tshirt_too_long(self, tshirt_client, field):
        with allure.step(f"Подготовка данных: поле {field} = 'a'*256"):
            dto = {
                "name": "Test",
                "color": "red",
                "size": "L",
                "price": 1000,
                "article": self._unique_article("LONG"),
                "material": "cotton",
                "countryOfProduction": "China",
                "description": "desc",
                "image": ""
            }
            long_value = "a" * 256
            dto[field] = long_value

        with allure.step("Отправка POST-запроса"):
            resp = tshirt_client.create_tshirt(dto)
            allure.attach(str(resp.status_code), name="HTTP статус", attachment_type=allure.attachment_type.TEXT)
            allure.attach(resp.text, name="Тело ответа", attachment_type=allure.attachment_type.JSON)

        if resp.status_code == 400:
            with allure.step("Проверка наличия сообщения об ошибке"):
                error = resp.json()
                assert "message" in error
        else:
            with allure.step("Проверка успешного создания (возможно, поле было обрезано)"):
                assert resp.status_code == 201
                data = resp.json()
                assert "id" in data
                with allure.step("Удаление созданной футболки"):
                    tshirt_client.delete_tshirt(data["id"])

    @allure.story("Негативные сценарии")
    @allure.title("Создание футболки с некорректным файлом картинки (текстовый файл)")
    @allure.severity(allure.severity_level.MINOR)
    @allure.description("""
        Цель: Проверить, что API принимает любой файл, даже не являющийся изображением.
        Создаётся временный текстовый файл и передаётся как картинка.
        Ожидается успешное создание (201), так как сервер не проверяет содержимое файла.
    """)
    def test_create_tshirt_invalid_picture(self, tshirt_client, tmp_path):
        with allure.step("Создание временного текстового файла"):
            fake_pic = tmp_path / "fake.txt"
            fake_pic.write_text("Это не картинка")
            allure.attach("Это не картинка", name="Содержимое fake.txt", attachment_type=allure.attachment_type.TEXT)

        with allure.step("Подготовка данных для создания футболки"):
            dto = {
                "name": "Invalid pic",
                "color": "white",
                "size": "S",
                "price": 500,
                "article": self._unique_article("PIC"),
                "material": "poly",
                "countryOfProduction": "USA",
                "description": "bad pic",
                "image": ""
            }

        with allure.step("Отправка POST-запроса с некорректным файлом"):
            resp = tshirt_client.create_tshirt(dto, picture_path=str(fake_pic))
            allure.attach(str(resp.status_code), name="HTTP статус", attachment_type=allure.attachment_type.TEXT)
            allure.attach(resp.text, name="Тело ответа", attachment_type=allure.attachment_type.JSON)

        with allure.step("Проверка статуса ответа = 201 (сервер принимает любой файл)"):
            assert resp.status_code == 201

        data = resp.json()
        with allure.step("Проверка наличия ID и удаление созданной футболки"):
            assert "id" in data
            tshirt_client.delete_tshirt(data["id"])