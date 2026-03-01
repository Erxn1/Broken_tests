import allure
import pytest

@pytest.mark.usefixtures("prepared_news")
class TestGetNews:
    @allure.title("При запросе с валидными параметрами возвращается список новостей")
    def test_get_news_test(self, news_client):
        size = 10
        resp = news_client.get_news_list(0, size)
        assert resp.status_code == 200
        data = resp.json()
        assert isinstance(data, list)
        assert len(data) <= size
        for item in data:
            assert "id" in item
            assert "header" in item
            assert "description" in item
            assert isinstance(item["id"], int)
            assert isinstance(item["header"], str)
            assert isinstance(item["description"], str)

    @pytest.mark.parametrize("page,size,expected_status", [
        (0, 10, 200),
        (1, 5, 200),
        (0, 1, 200),
        (0, 100, 200),
        (-1, 10, 400),
        (0, -5, 400),
        (0, 0, 400),
    ])
    def test_get_news_list_parametrize(self, news_client, page, size, expected_status):
        resp = news_client.get_news_list(page, size)
        assert resp.status_code == expected_status
        if expected_status == 200:
            data = resp.json()
            assert isinstance(data, list)
            assert len(data) <= size