from utils.base_client import BaseClient
from endpoints import news_list, news_detail

class NewsClient(BaseClient):
    def create_news(self, header: str, description: str):
        url = self._url(news_list())
        payload = {"header": header, "description": description}
        return self._post_json(url, json=payload)

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

    def create_news_raw(self, payload: dict):
        return self._post_json(self._url(news_list()), json=payload)