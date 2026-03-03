import requests

class BaseClient:
    def __init__(self, base_url: str):
        self.base_url = base_url.rstrip('/')
        self.session = requests.Session()

    def _url(self, path: str) -> str:
        return f"{self.base_url}{path}"

    def _post_json(self, url, json=None, **kwargs):
        headers = kwargs.pop('headers', {})
        headers['Content-Type'] = 'application/json'
        return self.session.post(url, json=json, headers=headers, **kwargs)