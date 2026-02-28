import pytest
import allure

@allure.feature("Новости")

class TestCreateNews:

    @allure.title("Создание новости с корректными данными")

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

        # Удаляем за собой
        del_resp = news_client.delete_news(news_id)
        assert del_resp.status_code == 204

    @allure.title("Позитивный сценарий: пустой заголовок")

    def test_create_news_empty_header(self, news_client):
        resp = news_client.create_news("", "Описание")
        assert resp.status_code == 201
        error = resp.json()

    @allure.title("Позитивный сценарий: пустое описание.")

    def test_create_news_empty_description(self, news_client):
        resp = news_client.create_news("Заголовок", "")
        assert resp.status_code == 201
        error = resp.json()

    @allure.title("Негативный сценарий: отсутствует поле header.")
    def test_create_news_missing_header(self, news_client):
        url = news_client._url("/news")
        payload = {"description": "Описание"}
        resp = news_client.session.post(url, json=payload)
        assert resp.status_code == 400
        error = resp.json()
        assert "message" in error
        assert "type" in error

    @allure.title("Негативный сценарий: отсутствует поле description.")
    def test_create_news_missing_description(self, news_client):
        url = news_client._url("/news")
        payload = {"header": "Заголовок"}
        resp = news_client.session.post(url, json=payload)
        assert resp.status_code == 400
        error = resp.json()
        assert "message" in error
        assert "type" in error

    @allure.title("Негативный сценарий: лишние поля игнорируются.")
    def test_create_news_extra_fields(self, news_client):
        url = news_client._url("/news")
        payload = {
            "header": "Заголовок",
            "description": "Описание",
            "extra": "лишнее поле"
        }
        resp = news_client.session.post(url, json=payload)
        assert resp.status_code == 201
        data = resp.json()
        assert data["header"] == "Заголовок"
        assert data["description"] == "Описание"
        assert "extra" not in data
        # Очистка
        news_client.delete_news(data["id"])

    @pytest.mark.parametrize("field,value", [
        ("header", "a" * 256),       # если ограничение 255 символов
        ("description", "b" * 1001)   # если ограничение 1000 символов
    ])
    @allure.title("Негативный сценарий: превышение максимальной длины поля.")
    def test_create_news_too_long(self, news_client, field, value):
        payload = {"header": "h", "description": "d", field: value}
        resp = news_client.session.post(news_client._url("/news"), json=payload)
        assert resp.status_code == 400
        error = resp.json()
        assert "message" in error
        assert "type" in error