from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import requests
from bs4 import BeautifulSoup

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

# Function to scrape news from free sources
def scrape_news():
    news = []

    # 1️⃣ Football (ESPN)
    try:
        url = "https://www.espn.com/soccer/"
        resp = requests.get(url)
        soup = BeautifulSoup(resp.text, "html.parser")
        articles = soup.select("section.contentItem")[:5]
        for a in articles:
            title_tag = a.select_one("h1, h2, h3")
            link_tag = a.select_one("a")
            img_tag = a.select_one("img")
            if title_tag and link_tag:
                news.append({
                    "title": title_tag.get_text(strip=True),
                    "url": link_tag.get("href"),
                    "image": img_tag["src"] if img_tag else "",
                    "sport": "Football"
                })
    except Exception as e:
        print("Football scrape error:", e)

    # 2️⃣ Cricket (CricBuzz)
    try:
        url = "https://www.cricbuzz.com/cricket-news"
        resp = requests.get(url)
        soup = BeautifulSoup(resp.text, "html.parser")
        articles = soup.select("div.cb-nws-intr")[:5]
        for a in articles:
            title_tag = a.select_one("a")
            if title_tag:
                news.append({
                    "title": title_tag.get_text(strip=True),
                    "url": "https://www.cricbuzz.com" + title_tag["href"],
                    "image": "",
                    "sport": "Cricket"
                })
    except Exception as e:
        print("Cricket scrape error:", e)

    # 3️⃣ Basketball (NBA)
    try:
        url = "https://www.nba.com/news"
        resp = requests.get(url)
        soup = BeautifulSoup(resp.text, "html.parser")
        articles = soup.select("section.Article_card__")[:5]
        for a in articles:
            title_tag = a.select_one("h2")
            link_tag = a.select_one("a")
            img_tag = a.select_one("img")
            if title_tag and link_tag:
                news.append({
                    "title": title_tag.get_text(strip=True),
                    "url": "https://www.nba.com" + link_tag["href"],
                    "image": img_tag["src"] if img_tag else "",
                    "sport": "Basketball"
                })
    except Exception as e:
        print("Basketball scrape error:", e)

    # 4️⃣ Tennis (ATP)
    try:
        url = "https://www.atptour.com/en/news"
        resp = requests.get(url)
        soup = BeautifulSoup(resp.text, "html.parser")
        articles = soup.select("div.news-item")[:5]
        for a in articles:
            title_tag = a.select_one("a")
            img_tag = a.select_one("img")
            if title_tag:
                news.append({
                    "title": title_tag.get_text(strip=True),
                    "url": "https://www.atptour.com" + title_tag["href"],
                    "image": img_tag["src"] if img_tag else "",
                    "sport": "Tennis"
                })
    except Exception as e:
        print("Tennis scrape error:", e)

    # 5️⃣ Others - placeholder minor sports
    others = [
        {"title": "Olympics Updates", "url": "#", "image": "", "sport": "Others"},
        {"title": "Swimming Highlights", "url": "#", "image": "", "sport": "Others"}
    ]
    news.extend(others)

    return news

@app.get("/api/news")
def get_news():
    return scrape_news()
