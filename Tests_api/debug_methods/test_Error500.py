import requests

def test_error_500(base_url):
    response=requests.get(f"{base_url}/api/error500")
    assert response.status_code == 500, f"Ждал код 500 получил :{response.status_code}"
    assert response.text, "Тело ответа пустое"
    assert "Статус кода: 500" in response.text, "В ответе нет ожидаемого сообщения"