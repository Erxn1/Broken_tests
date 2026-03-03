import pytest
import allure


@allure.epic("Управление новостями")
@allure.feature("Новости")
@allure.story("Создание новостей")
class TestCreateNews:

    @allure.title("Создание новости с корректными данными")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.description("Проверяем успешное создание новости с заполненными заголовком и описанием, затем проверяем, что новость действительно создана (получение по id) и удаляем её.")
    def test_create_news_success(self, news_client):
        header = "Заголовок тестовой новости"
        description = "Описание тестовой новости"

        resp = news_client.create_news(header, description)
        assert resp.status_code == 201
        data = resp.json()
        assert data["header"] == header
        assert data["description"] == description
        assert "id" in data

        news_id = data["id"]
        get_resp = news_client.get_news_by_id(news_id)
        assert get_resp.status_code == 200
        assert get_resp.json() == data

        del_resp = news_client.delete_news(news_id)
        assert del_resp.status_code == 204

    @allure.title("Позитивный сценарий: пустой заголовок")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.description("Проверяем, что можно создать новость с пустым заголовком (строка нулевой длины).")
    def test_create_news_empty_header(self, news_client):
        resp = news_client.create_news("", "Описание")
        assert resp.status_code == 201
        data = resp.json()
        assert data["header"] == ""
        assert data["description"] == "Описание"
        assert "id" in data

        del_resp = news_client.delete_news(data["id"])
        assert del_resp.status_code == 204

    @allure.title("Позитивный сценарий: пустое описание.")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.description("Проверяем, что можно создать новость с пустым описанием (строка нулевой длины).")
    def test_create_news_empty_description(self, news_client):
        resp = news_client.create_news("Заголовок", "")
        assert resp.status_code == 201
        data = resp.json()
        assert data["header"] == "Заголовок"
        assert data["description"] == ""
        assert "id" in data

        del_resp = news_client.delete_news(data["id"])
        assert del_resp.status_code == 204

    @allure.title("Негативный сценарий: отсутствует поле header.")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.description("Проверяем, что при отсутствии поля 'header' сервер возвращает 400 с сообщением об ошибке.")
    def test_create_news_missing_header(self, news_client):
        payload = {"description": "Описание"}
        resp = news_client.create_news_raw(payload)
        assert resp.status_code == 400
        error = resp.json()
        assert "message" in error
        assert "type" in error

    @allure.title("Негативный сценарий: отсутствует поле description.")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.description("Проверяем, что при отсутствии поля 'description' сервер возвращает 400 с сообщением об ошибке.")
    def test_create_news_missing_description(self, news_client):
        payload = {"header": "Заголовок"}
        resp = news_client.create_news_raw(payload)
        assert resp.status_code == 400
        error = resp.json()
        assert "message" in error
        assert "type" in error

    @allure.title("Приведение типов: число в поле header преобразуется в строку")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.description("Проверяем, что если передать число в поле header, сервер преобразует его в строку и создаёт новость.")
    def test_create_news_invalid_header(self, news_client):
        payload = {"description": "valid", "header": 123}
        resp = news_client.create_news_raw(payload)
        assert resp.status_code == 201
        data = resp.json()
        assert data["header"] == "123"
        assert isinstance(data["header"], str)
        assert data["description"] == "valid"
        assert 'id' in data

        del_resp = news_client.delete_news(data["id"])
        assert del_resp.status_code == 204

    @allure.title("Приведение типов: число в поле description преобразуется в строку")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.description("Проверяем, что если передать число в поле description, сервер преобразует его в строку и создаёт новость.")
    def test_create_news_invalid_description(self, news_client):
        payload = {"description": 123, "header": "valid"}
        resp = news_client.create_news_raw(payload)
        assert resp.status_code == 201
        data = resp.json()
        assert data["header"] == "valid"
        assert data["description"] == "123"
        assert isinstance(data["description"], str)
        assert 'id' in data

        del_resp = news_client.delete_news(data["id"])
        assert del_resp.status_code == 204

    @allure.title("Негативный сценарий: лишние поля игнорируются.")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.description("Проверяем, что дополнительные поля в запросе не влияют на создание новости (игнорируются).")
    def test_create_news_extra_fields(self, news_client):
        payload = {
            "header": "Заголовок",
            "description": "Описание",
            "extra": "лишнее поле"
        }
        resp = news_client.create_news_raw(payload)
        assert resp.status_code == 201
        data = resp.json()
        assert data["header"] == "Заголовок"
        assert data["description"] == "Описание"
        assert "extra" not in data

        del_resp = news_client.delete_news(data["id"])
        assert del_resp.status_code == 204

    @pytest.mark.parametrize("header,description", [
        ("a" * 256, "норм описание"),
        ("норм заголовок", "b" * 256),
        ("a" * 256, "b" * 256)
    ])
    @allure.title("Негативный сценарий: превышение максимальной длины поля. 256 символов")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.description("Проверяем, что при отправке поля длиной 256 символов (больше допустимых 255) сервер возвращает 400.")
    def test_create_news_too_long(self, news_client, header, description):
        payload = {"header": header, "description": description}
        resp = news_client.create_news_raw(payload)
        assert resp.status_code == 400
        error = resp.json()
        assert "message" in error
        assert "type" in error

    @pytest.mark.parametrize("header,description", [
        ("a" * 255, "норм описание"),
        ("норм заголовок", "b" * 255),
        ("a" * 255, "b" * 255)
    ])
    @allure.title("Позитивный сценарий: Верхняя граница 255 символов длины поля")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.description("Проверяем, что поля длиной 255 символов (максимально допустимое) проходят успешно.")
    def test_create_news_too_long_valid(self, news_client, header, description):
        payload = {"header": header, "description": description}
        resp = news_client.create_news_raw(payload)
        assert resp.status_code == 201
        data = resp.json()
        assert data["header"] == header
        assert data["description"] == description
        assert 'id' in data

        del_resp = news_client.delete_news(data["id"])
        assert del_resp.status_code == 204