import requests
from bs4 import BeautifulSoup
from datetime import datetime

def generate_daily_news():
    """
    Scrape sports news from free sources (BBC Sport and ESPN as examples)
    and return a dict with 'trending' and 'latest'.
    """
    trending = []
    latest = []

    try:
        # Example 1: BBC Sport football
        bbc_url = "https://www.bbc.com/sport/football"
        res = requests.get(bbc_url)
        soup = BeautifulSoup(res.text, "html.parser")
        
        articles = soup.select("a.gs-c-promo-heading")[:5]  # top 5 trending
        for a in articles:
            title = a.get_text(strip=True)
            link = a['href']
            if not link.startswith("http"):
                link = "https://www.bbc.com" + link
            trending.append({
                "title": title,
                "content": title,  # BBC often doesn't have content preview; using title
                "link": link
            })

        # Example 2: ESPN latest news
        espn_url = "https://www.espn.com/espn/latestnews"
        res = requests.get(espn_url)
        soup = BeautifulSoup(res.text, "html.parser")

        articles = soup.select("section.contentItem")[:5]  # top 5 latest
        for art in articles:
            title_tag = art.find("h1") or art.find("h2") or art.find("a")
            link_tag = art.find("a", href=True)
            if title_tag and link_tag:
                title = title_tag.get_text(strip=True)
                link = link_tag['href']
                if not link.startswith("http"):
                    link = "https://www.espn.com" + link
                latest.append({
                    "title": title,
                    "content": title,
                    "link": link
                })

    except Exception as e:
        print("Error fetching news:", e)

    # Return both trending and latest
    return {
        "trending": trending,
        "latest": latest
    }
