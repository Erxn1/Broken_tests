from utils.base_client import BaseClient
from endpoints import news_list, news_detail


# Раздел Новости

class NewsClient(BaseClient):
    def create_news(self, header: str, description: str):
        url = self._url(news_list())
        payload = {"header": header, "description": description}
        return self.session.post(url, json=payload)

    def get_news_list(self, page: int = 0, size: int = 10):
        url = self._url(news_list())
        params = {"page": page, "size": size}
        return self.session.get(url, params=params)

    def get_news_by_id(self, news_id: int):
        url = self._url(news_detail(news_id))
        return self.session.get(url)

    def delete_news(self, news_id: int):
        url = self._url(news_detail(news_id))
        return self.session.delete(url)