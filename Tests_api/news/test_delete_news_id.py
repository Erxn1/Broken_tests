import allure
import pytest

from conftest import news_client


@allure.epic("Управление новостями")
@allure.feature("Удаление новостей")
class TestDeleteNews:

    @allure.title("Успешное удаление новости")
    @allure.story("Позитивный сценарий удаления")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.description("Проверка успешного удаления существующей новости: создаём новость, удаляем её, затем проверяем, что она больше не доступна.")
    def test_delete_valid_news(self, news_client):

        create_resp = news_client.create_news("Header", "Description")
        assert create_resp.status_code == 201
        news_id = create_resp.json()["id"]

        del_resp = news_client.delete_news(news_id)
        assert del_resp.status_code == 204

        get_resp = news_client.get_news_by_id(news_id)
        assert get_resp.status_code == 404

    @pytest.mark.parametrize("news_id", [
        999999999,
        "string",
        "",
        -1,
        0,
        1.5,
        " 999999999",
        "999999999  ",
        "12 3",
        "@#$",
        "null",
    ])
    @allure.title("Негативный сценарий: удаление с невалидным id {news_id}")
    @allure.story("Негативные сценарии удаления")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.description("Проверка, что API корректно обрабатывает попытки удаления с некорректными идентификаторами (несуществующий id, строка, спецсимволы и т.д.).")
    def test_delete_invalid_id(self, news_client, news_id):
        del_resp = news_client.delete_news(news_id)
        assert del_resp.status_code == 404
        error = del_resp.json()
        assert "message" in error