
# Раздел с новостями
BASE_NEWS_PATH = "/news"

def news_list():
    return BASE_NEWS_PATH

def news_detail(news_id: int):
    return f"{BASE_NEWS_PATH}/{news_id}"


# Раздел с футболками
BASE_TSHIRT_PATH = "/t-shirt"

def tshirt_list():
    return BASE_TSHIRT_PATH

def tshirt_detail(tshirt_id: int):
    return f"{BASE_TSHIRT_PATH}/{tshirt_id}"