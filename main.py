from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import feedparser

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

RSS_FEEDS = [
    "https://www.espn.com/espn/rss/news",
    "https://www.bbc.com/sport/rss.xml"
]

def detect_category(title, link):
    t = title.lower()
    l = link.lower()

    if "soccer" in t or "/football/" in l or "premier league" in t:
        return "Soccer"
    if "nfl" in t or "/nfl/" in l or "pro bowl" in t:
        return "Football"
    if "nba" in t or "/nba/" in l or "basketball" in t:
        return "Basketball"
    if "cricket" in t or "/cricket/" in l or "ashes" in t:
        return "Cricket"
    if "golf" in t or "/golf/" in l:
        return "Golf"
    if "tennis" in t or "/tennis/" in l:
        return "Tennis"

    return "Others"

@app.get("/api/news")
def get_news():
    news = []

    for feed_url in RSS_FEEDS:
        feed = feedparser.parse(feed_url)

        for entry in feed.entries[:20]:
            title = entry.get("title", "")
            link = entry.get("link", "")
            summary = entry.get("summary", "")
            published = entry.get("published", "")

            category = detect_category(title, link)

            news.append({
                "title": title,
                "content": summary,
                "link": link,
                "published": published,
                "category": category
            })

    return news
