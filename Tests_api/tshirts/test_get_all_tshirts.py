import allure
import pytest


@allure.epic("Управление футболками")
@allure.feature("Футболки")
@allure.story("Получение списка всех футболок")
class TestGetAllTshirts:

    @allure.title("Получение списка с пагинацией по умолчанию")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.description("""
        Цель: Проверить, что GET /t-shirt/all возвращает 200 и список футболок с параметрами по умолчанию (page=0, size=10).
        Шаги:
        1. Выполнить запрос без указания параметров.
        2. Проверить статус 200.
        3. Проверить, что ответ — это список, и его длина не превышает size по умолчанию (10).
        4. Проверить структуру каждого элемента (наличие обязательных полей).
        Ожидаемый результат: Успешное получение списка.
    """)
    def test_get_all_default(self, tshirt_client):
        with allure.step("Выполнение GET-запроса /t-shirt/all с параметрами по умолчанию"):
            resp = tshirt_client.get_tshirt_list()
            allure.attach(str(resp.status_code), name="HTTP статус", attachment_type=allure.attachment_type.TEXT)
            allure.attach(resp.text, name="Тело ответа", attachment_type=allure.attachment_type.JSON)

        with allure.step("Проверка статуса 200"):
            assert resp.status_code == 200

        data = resp.json()
        with allure.step("Проверка, что ответ является списком"):
            assert isinstance(data, list), "Ответ должен быть списком"

        with allure.step("Проверка длины списка (не более 10)"):
            assert len(data) <= 10, f"Длина списка {len(data)} превышает ожидаемую 10"

        if data:
            with allure.step("Проверка структуры первого элемента"):
                item = data[0]
                expected_fields = ["id", "article", "name", "size", "color", "material", "countryOfProduction", "price"]
                for field in expected_fields:
                    assert field in item, f"Поле {field} отсутствует в элементе"

    @allure.title("Получение списка с явными параметрами page и size")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.parametrize("page,size", [
        (0, 5),
        (1, 3),
        (0, 20),
        (2, 2)
    ])
    def test_get_all_with_params(self, tshirt_client, page, size):
        with allure.step(f"Выполнение GET-запроса с page={page}, size={size}"):
            resp = tshirt_client.get_tshirt_list(page=page, size=size)
            allure.attach(str(resp.status_code), name="HTTP статус", attachment_type=allure.attachment_type.TEXT)
            allure.attach(resp.text, name="Тело ответа", attachment_type=allure.attachment_type.JSON)

        with allure.step("Проверка статуса 200"):
            assert resp.status_code == 200

        data = resp.json()
        with allure.step("Проверка, что ответ является списком"):
            assert isinstance(data, list)

        with allure.step(f"Проверка длины списка (не более {size})"):
            assert len(data) <= size, f"Длина списка {len(data)} превышает {size}"

    @allure.title("Получение списка с невалидными параметрами")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.parametrize("page,size,expected_status", [
        (-1, 10, 400),
        (0, 0, 400),
        (0, -5, 400),
        ("abc", 10, 400),
        (0, "def", 400)
    ])
    def test_get_all_invalid_params(self, tshirt_client, page, size, expected_status):
        with allure.step(f"Выполнение GET-запроса с page={page}, size={size}"):
            resp = tshirt_client.get_tshirt_list(page=page, size=size)
            allure.attach(str(resp.status_code), name="HTTP статус", attachment_type=allure.attachment_type.TEXT)
            allure.attach(resp.text, name="Тело ответа", attachment_type=allure.attachment_type.JSON)

        with allure.step(f"Проверка статуса {expected_status}"):
            assert resp.status_code == expected_status, f"Ожидался {expected_status}, получен {resp.status_code}"

        if expected_status == 400:
            error = resp.json()
            assert error, "Тело ответа с ошибкой не должно быть пустым"
            # Дополнительно можно проверить, что в значениях есть ожидаемый текст (опционально)
            # Например:
            # error_text = str(error)
            # assert "must be greater than" in error_text

    @allure.title("Проверка, что после создания новой футболки она появляется в списке")
    @allure.severity(allure.severity_level.NORMAL)
    def test_new_tshirt_appears_in_list(self, tshirt_client, created_tshirt):
        tshirt_id = created_tshirt["id"]
        page = 0
        size = 100  # разумный размер страницы
        max_pages = 100  # ограничение, чтобы не уйти в бесконечный цикл
        found = False

        with allure.step("Постраничный перебор списка футболок для поиска созданной"):
            for page in range(max_pages):
                resp = tshirt_client.get_tshirt_list(page=page, size=size)
                assert resp.status_code == 200, f"Не удалось получить страницу {page}"
                data = resp.json()
                if not data:  # пустая страница — дальше нет записей
                    break
                ids = [item["id"] for item in data]
                if tshirt_id in ids:
                    found = True
                    break

        assert found, f"Футболка с ID {tshirt_id} не найдена в первых {max_pages} страницах по {size} записей"