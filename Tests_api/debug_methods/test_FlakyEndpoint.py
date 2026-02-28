import requests

def test_error_500_flaky(base_url):
    response=requests.get(f"{base_url}/api/flakyEndpoint")
    assert response.status_code == 200, f"Ждал код 200 получил :{response.status_code}"
