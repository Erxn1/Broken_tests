import pytest
import allure


@allure.epic("Управление новостями")
@allure.feature("Получение новости по ID")
class TestGetNewsById:

    @allure.story("Позитивные сценарии")
    @allure.title("Получение существующей новости по ID")
    @allure.description("Создаём новость, затем запрашиваем её по ID и проверяем, что данные совпадают.")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_get_news_by_id_valid(self, news_client):

        header = "Заголовок для теста получения"
        description = "Описание для теста получения"
        create_resp = news_client.create_news(header, description)
        assert create_resp.status_code == 201
        news_id = create_resp.json()["id"]

        with allure.step(f"GET /news/{news_id}"):
            get_resp = news_client.get_news_by_id(news_id)
        assert get_resp.status_code == 200
        data = get_resp.json()
        assert data["id"] == news_id
        assert data["header"] == header
        assert data["description"] == description

        del_resp = news_client.delete_news(news_id)
        assert del_resp.status_code == 204

    @pytest.mark.parametrize("invalid_id", [
        999999999,
        -1,
        0,
        "string",
        "",
        " 999999999",
        "999999999  ",
        "12 3",
        "@#$",
        "null",
        1.5,
    ])
    @allure.story("Негативные сценарии")
    @allure.title("Получение новости с невалидным ID: {invalid_id}")
    @allure.description("Проверяем, что запрос новости с некорректным или несуществующим ID возвращает 404 и сообщение об ошибке.")
    @allure.severity(allure.severity_level.NORMAL)
    def test_get_news_by_id_invalid(self, news_client, invalid_id):
        resp = news_client.get_news_by_id(invalid_id)
        assert resp.status_code == 404
        error = resp.json()
        assert "message" in error
        assert "type" in error