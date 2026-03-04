import json
import os
from endpoints import tshirt_create, tshirt_list_all, tshirt_detail
from utils.base_client import BaseClient

class TshirtClient(BaseClient):

    def create_tshirt(self, dto: dict, picture_path: str = None):
        url = self._url(tshirt_create())
        files = {
            'dto': (None, json.dumps(dto, ensure_ascii=False), 'application/json')
        }
        if picture_path and os.path.isfile(picture_path):
            filename = os.path.basename(picture_path)
            content_type = 'image/jpeg'
            if filename.lower().endswith('.png'):
                content_type = 'image/png'
            elif filename.lower().endswith('.gif'):
                content_type = 'image/gif'
            with open(picture_path, 'rb') as f:
                file_content = f.read()
            files['picture'] = (filename, file_content, content_type)

        return self.session.post(url, files=files)

    def create_tshirt_raw(self, dto: dict, picture_content: bytes = None, picture_filename: str = None):
        url = self._url(tshirt_create())
        files = {
            'dto': (None, json.dumps(dto, ensure_ascii=False), 'application/json')
        }
        if picture_content and picture_filename:
            files['picture'] = (picture_filename, picture_content, 'image/jpeg')
        return self.session.post(url, files=files)

    def get_tshirt_list(self, page: int = 0, size: int = 10):
        url = self._url(tshirt_list_all())
        params = {"page": page, "size": size}
        return self.session.get(url, params=params)

    def get_tshirt_by_id(self, tshirt_id: int):
        url = self._url(tshirt_detail(tshirt_id))
        return self.session.get(url)

    def delete_tshirt(self, tshirt_id: int):
        url = self._url(tshirt_detail(tshirt_id))
        return self.session.delete(url)

    def update_tshirt(self, tshirt_id: int, dto: dict):
        url = self._url(tshirt_detail(tshirt_id))
        return self.session.put(url, json=dto)