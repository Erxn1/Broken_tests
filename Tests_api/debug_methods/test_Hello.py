import requests

def test_hello(base_url):
    response = requests.get(f"{base_url}/api/hello")
    assert response.status_code == 200, f"Ожидаю статус код 200, но получил : {response.status_code}"
    assert response.text, f"Тело ответа не пустое"
    assert "Hello, Stasyan" in response.text, f"Ожидаю сообщение 'Hello, Stasyan', но получил : {response.text}"
