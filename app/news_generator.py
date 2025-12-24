import requests
from bs4 import BeautifulSoup

def generate_daily_news():
    news = []

    # Example: Scrape BBC Sport Football headlines
    url = "https://www.bbc.com/sport/football"
    resp = requests.get(url)
    soup = BeautifulSoup(resp.text, "html.parser")

    for item in soup.select("a.gs-c-promo-heading")[:10]:
        title = item.get_text(strip=True)
        link = item["href"]
        if not link.startswith("http"):
            link = f"https://www.bbc.com{link}"
        news.append({"title": title, "content": "", "url": link})

    return news

def generate_trending_news():
    trending = []

    # Example: Scrape ESPN trending headlines
    url = "https://www.espn.com/"
    resp = requests.get(url)
    soup = BeautifulSoup(resp.text, "html.parser")

    for item in soup.select("section.headlineStack li a")[:10]:
        title = item.get_text(strip=True)
        link = item["href"]
        if not link.startswith("http"):
            link = f"https://www.espn.com{link}"
        trending.append({"title": title, "url": link})

    return trending
