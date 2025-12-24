import feedparser
import re
from datetime import datetime

RSS_FEEDS = [
    "https://www.espn.com/espn/rss/news",
    "https://feeds.bbci.co.uk/sport/rss.xml",
    "https://www.skysports.com/rss/12040"
]

def detect_category(title, summary):
    text = f"{title} {summary}".lower()

    if any(word in text for word in [
        "football", "soccer", "fifa", "premier league",
        "champions league", "la liga", "manchester", "arsenal"
    ]):
        return "Soccer"

    if any(word in text for word in [
        "cricket", "ipl", "odi", "t20", "test match", "icc", "bcci"
    ]):
        return "Cricket"

    return "Other"

def rewrite_summary(text):
    text = re.sub('<[^<]+?>', '', text)
    text = text.replace("Read more", "").strip()

    if len(text) > 250:
        text = text[:250] + "..."

    return text

def generate_daily_news():
    articles = []

    for url in RSS_FEEDS:
        feed = feedparser.parse(url)

        for entry in feed.entries[:5]:
            article = {
                "title": entry.get("title", ""),
                "content": rewrite_summary(entry.get("summary", "")),
                "link": entry.get("link", ""),
                "published": entry.get("published", ""),
                "category": detect_category(
                    entry.get("title", ""),
                    entry.get("summary", "")
                )
            }
            articles.append(article)

    return articles

def get_trending_news():
    news = generate_daily_news()
    return sorted(news, key=lambda x: len(x["title"]), reverse=True)[:5]
