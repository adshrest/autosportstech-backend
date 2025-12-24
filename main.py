from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import feedparser

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

SPORT_FEEDS = {
    "Soccer": [
        "https://www.bbc.com/sport/football/rss.xml",
        "https://www.espn.com/espn/rss/soccer/news"
    ],
    "Football": [
        "https://www.espn.com/espn/rss/nfl/news"
    ],
    "Basketball": [
        "https://www.espn.com/espn/rss/nba/news"
    ],
    "Cricket": [
        "https://www.bbc.com/sport/cricket/rss.xml"
    ],
    "Tennis": [
        "https://www.bbc.com/sport/tennis/rss.xml"
    ],
    "Golf": [
        "https://www.espn.com/espn/rss/golf/news"
    ]
}

@app.get("/api/news")
def get_news():
    all_news = []

    for sport, feeds in SPORT_FEEDS.items():
        for feed_url in feeds:
            feed = feedparser.parse(feed_url)

            for entry in feed.entries[:10]:
                all_news.append({
                    "sport": sport,
                    "title": entry.get("title", ""),
                    "content": entry.get("summary", ""),
                    "url": entry.get("link", ""),
                    "published": entry.get("published", ""),
                    "image": (
                        entry.media_content[0]["url"]
                        if "media_content" in entry else ""
                    )
                })

    return all_news
