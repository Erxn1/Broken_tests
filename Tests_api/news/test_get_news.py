from conftest import news_client


class GetNews:

    def get_news_test(self, news_client):
        page = 0
        size = 10
        resp = news_client.get_news_list(page, size)
        assert resp.status_code == 200