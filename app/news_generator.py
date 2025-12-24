import requests
from bs4 import BeautifulSoup

SPORTS_NEWS_URLS = [
    "https://www.espn.com/espn/latestnews",
    "https://www.skysports.com/football/news",
    # Add more sports news URLs here
]

def fetch_sports_news():
    trending = []
    latest = []

    for url in SPORTS_NEWS_URLS:
        try:
            res = requests.get(url, timeout=10)
            soup = BeautifulSoup(res.text, "html.parser")

            # Example selectors for titles, links, images, and description
            articles = soup.find_all("article")[:10]  # first 10 articles
            for a in articles:
                title_tag = a.find("a")
                if not title_tag:
                    continue
                title = title_tag.get_text(strip=True)
                link = title_tag['href']
                if link.startswith("/"):
                    link = f"{url.split('/')[0]}//{url.split('/')[2]}{link}"

                # Optional image
                img_tag = a.find("img")
                img = img_tag['src'] if img_tag else ""

                # Optional description / summary
                desc_tag = a.find("p")
                description = desc_tag.get_text(strip=True) if desc_tag else ""

                item = {
                    "title": title,
                    "content": description,
                    "link": link,
                    "image": img
                }
                latest.append(item)

            trending = latest[:5]  # top 5 trending

        except Exception as e:
            print("Error fetching news from", url, e)

    return {"trending": trending, "latest": latest}
