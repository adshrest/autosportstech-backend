import requests
from bs4 import BeautifulSoup

HEADERS = {
    "User-Agent": "Mozilla/5.0"
}

def fetch_bbc(section, sport):
    url = f"https://www.bbc.com/sport/{section}"
    res = requests.get(url, headers=HEADERS, timeout=10)
    soup = BeautifulSoup(res.text, "html.parser")
    items = []

    for article in soup.select("div.gs-c-promo")[:8]:
        title = article.select_one("h3")
        link = article.select_one("a")
        summary = article.select_one("p")
        img = article.select_one("img")

        if not title or not link:
            continue

        items.append({
            "sport": sport,
            "title": title.text.strip(),
            "content": summary.text.strip() if summary else "",
            "url": "https://www.bbc.com" + link.get("href"),
            "image": img.get("src") if img else ""
        })

    return items


def fetch_espn(path, sport):
    url = f"https://www.espn.com/{path}"
    res = requests.get(url, headers=HEADERS, timeout=10)
    soup = BeautifulSoup(res.text, "html.parser")
    items = []

    for article in soup.select("section.contentItem")[:8]:
        title = article.select_one("h2")
        link = article.select_one("a")
        img = article.select_one("img")

        if not title or not link:
            continue

        items.append({
            "sport": sport,
            "title": title.text.strip(),
            "content": "",
            "url": "https://www.espn.com" + link.get("href"),
            "image": img.get("src") if img else ""
        })

    return items


def get_all_news():
    news = []

    # Football (UK)
    news += fetch_bbc("football", "Football")

    # Soccer (International)
    news += fetch_bbc("football", "Soccer")

    # Cricket
    news += fetch_bbc("cricket", "Cricket")

    # Basketball
    news += fetch_espn("nba", "Basketball")

    # Tennis
    news += fetch_bbc("tennis", "Tennis")

    # Fallback
    for item in news:
        if "sport" not in item or not item["sport"]:
            item["sport"] = "Others"

    return news
