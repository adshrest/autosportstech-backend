from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import feedparser

app = FastAPI()

origins = [
    "https://sportsread.netlify.app",
    "http://localhost:8080",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

RSS_FEEDS = {
    "Football": "https://www.espn.com/espn/rss/soccer/news",
    "Cricket": "https://www.espncricinfo.com/rss/content/story/feeds/0.xml",
    "Basketball": "https://www.espn.com/espn/rss/nba/news",
    "Tennis": "https://www.atptour.com/en/rss/news",
}

# Others can be empty placeholder
OTHERS = [
    {"title": "Olympics Updates", "url": "#", "image": "", "sport": "Others"},
    {"title": "Swimming Highlights", "url": "#", "image": "", "sport": "Others"}
]

def fetch_news():
    news = []

    for sport, feed_url in RSS_FEEDS.items():
        try:
            feed = feedparser.parse(feed_url)
            for entry in feed.entries[:5]:
                news.append({
                    "title": entry.title,
                    "url": entry.link,
                    "image": getattr(entry, "media_content", [{}])[0].get("url", ""),
                    "sport": sport
                })
        except Exception as e:
            print(f"{sport} RSS fetch error:", e)

    news.extend(OTHERS)
    return news

@app.get("/api/news")
def get_news():
    return fetch_news()
