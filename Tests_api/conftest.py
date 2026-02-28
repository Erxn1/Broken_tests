import os
import pytest
from datetime import datetime
from utils.news_client import NewsClient

URLS = {
    "prod": "http://95.81.115.73:8085",
    "staging": "http://localhost:8080",
    "preprod": "https://preprod-api.example.com"
}

def pytest_addoption(parser):
    parser.addoption("--env", action="store", default="[prod]",
                     help="Окружение: prod, staging, preprod")

@pytest.fixture(scope="session")
def env(request):
    return request.config.getoption("--env")

@pytest.fixture
def base_url(env):
    url = URLS.get(env)
    if url is None:
        raise ValueError(f"Неизвестное окружение: {env}. Допустимые: {list(URLS.keys())}")
    return url

# Фикстура для клиента новостей
@pytest.fixture
def news_client(base_url):
    return NewsClient(base_url)

# Фикстура для создания тестовой новости и её автоудаления
@pytest.fixture
def created_news(news_client):
    resp = news_client.create_news("Test Header", "Test Description")
    assert resp.status_code == 200, f"Failed to create news: {resp.text}"
    news = resp.json()
    yield news
    del_resp = news_client.delete_news(news["id"])
    if del_resp.status_code not in (200, 204):
        print(f"Warning: Failed to delete news {news['id']}: {del_resp.text}")

# Хук для Allure
@pytest.hookimpl(tryfirstTrue)
def pytest_sessionstart(session):
    env = session.config.getoption("--env")
    base_url = URLS.get(env)
    if base_url is None:
        raise ValueError(f"Неизвестное окружение: {env}. Допустимые: {list(URLS.keys())}")

    allure_dir = "../allure-results"
    os.makedirs(allure_dir, exist_ok=True)

    env_data = {
        "Environment": env,
        "URL": base_url,
        "Test Run": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }

    with open(os.path.join(allure_dir, "environment.properties"), "w") as f:
        for key, value in env_data.items():
            f.write(f"{key}={value}\n")