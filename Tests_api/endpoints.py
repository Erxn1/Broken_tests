
# Раздел с новостями
BASE_NEWS_PATH = "/news"

def news_list():
    return BASE_NEWS_PATH

def news_detail(news_id: int):
    return f"{BASE_NEWS_PATH}/{news_id}"

