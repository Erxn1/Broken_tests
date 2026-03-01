import allure
import pytest

from conftest import news_client


class TestDeleteNews:
    @allure.title("Успешное удаление новости")
    def test_delete_valid_news(self, news_client):

        create_resp = news_client.create_news("Header", "Description")
        assert create_resp.status_code == 201
        news_id = create_resp.json()["id"]

        del_resp = news_client.delete_news(news_id)
        assert del_resp.status_code == 204

        get_resp = news_client.get_news_by_id(news_id)
        assert get_resp.status_code == 404

    @pytest.mark.parametrize("news_id", [
        999999999,  #Несуществующий id
        "string", #Строка вместо числа
        "",       #Пустая строка
        -1,
        0,
        1.5,
        " 999999999",   # пробел перед числом
        "999999999  ",   # пробел после
        "12 3",   # пробел внутри
        "@#$",    # спецсимволы
        "null",   # строка "null"
    ])
    @allure.title("Негативный сценарий: удаление с невалидным id {news_id}")
    def test_delete_invalid_id(self, news_client,news_id):
        del_resp = news_client.delete_news(news_id)
        assert del_resp.status_code == 404
        error = del_resp.json()
        assert "message" in error
