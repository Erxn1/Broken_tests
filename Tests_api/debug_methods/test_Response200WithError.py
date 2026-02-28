import requests

def test_response200_with_error (base_url):
    response = requests.get(f"{base_url}/api/response200WithError")
    assert response.status_code == 200
    assert response.text, f"Тело ответа пустое"
    assert "Error: Я не смогла" in response.text, "В ответе нет ожидаемого сообщения 'Error: Я не смогла'"
