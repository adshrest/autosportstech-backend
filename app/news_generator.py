import requests
from bs4 import BeautifulSoup

# Define sources for each sport
SOURCES = {
    "Football": [
        {"url": "https://www.bbc.com/sport/football", "base": "https://www.bbc.com"}
    ],
    "Soccer": [
        {"url": "https://www.goal.com/en", "base": "https://www.goal.com"}
    ],
    "Cricket": [
        {"url": "https://www.espncricinfo.com/", "base": "https://www.espncricinfo.com"}
    ],
    "Basketball": [
        {"url": "https://www.espn.com/nba/", "base": "https://www.espn.com"}
    ],
    "Tennis": [
        {"url": "https://www.atptour.com/en/news", "base": "https://www.atptour.com"}
    ]
}

def fetch_news_from_url(url, base_url, sport):
    try:
        resp = requests.get(url, timeout=10)
        resp.raise_for_status()
        soup = BeautifulSoup(resp.text, "html.parser")
        news_items = []

        if "bbc.com/sport/football" in url:
            articles = soup.select("div.gs-c-promo")[:10]
            for article in articles:
                title_tag = article.select_one("h3")
                link_tag = article.select_one("a")
                summary_tag = article.select_one("p")
                img_tag = article.select_one("img")
                if title_tag and link_tag:
                    news_items.append({
                        "sport": sport,
                        "title": title_tag.get_text(strip=True),
                        "content": summary_tag.get_text(strip=True) if summary_tag else "",
                        "url": base_url + link_tag.get("href") if link_tag.get("href").startswith("/") else link_tag.get("href"),
                        "image": img_tag.get("src") if img_tag else ""
                    })

        elif "goal.com" in url:
            articles = soup.select("article")[:10]
            for article in articles:
                title_tag = article.select_one("h3 a")
                summary_tag = article.select_one("p")
                img_tag = article.select_one("img")
                if title_tag:
                    news_items.append({
                        "sport": sport,
                        "title": title_tag.get_text(strip=True),
                        "content": summary_tag.get_text(strip=True) if summary_tag else "",
                        "url": base_url + title_tag.get("href") if title_tag.get("href").startswith("/") else title_tag.get("href"),
                        "image": img_tag.get("src") if img_tag else ""
                    })

        elif "espncricinfo.com" in url:
            articles = soup.select("section.news-card")[:10]
            for article in articles:
                title_tag = article.select_one("h2 a")
                summary_tag = article.select_one("p")
                img_tag = article.select_one("img")
                if title_tag:
                    news_items.append({
                        "sport": sport,
                        "title": title_tag.get_text(strip=True),
                        "content": summary_tag.get_text(strip=True) if summary_tag else "",
                        "url": title_tag.get("href"),
                        "image": img_tag.get("src") if img_tag else ""
                    })

        # Add other sports similarly if needed
        return news_items
    except Exception as e:
        print(f"Error fetching {sport} news from {url}: {e}")
        return []

def generate_daily_news():
    all_news = []
    for sport, sources in SOURCES.items():
        for source in sources:
            news = fetch_news_from_url(source["url"], source["base"], sport)
            all_news.extend(news)
    return all_news
