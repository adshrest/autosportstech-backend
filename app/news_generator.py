from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from bs4 import BeautifulSoup
import requests

app = FastAPI()

# Allow frontend access
origins = [
    "https://sportsread.netlify.app",
    "http://localhost:8080",
    "http://127.0.0.1:8080"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Helper function to scrape BBC Sport by category
def scrape_bbc_sport(url):
    try:
        r = requests.get(url)
        soup = BeautifulSoup(r.content, "html.parser")
        news_list = []

        articles = soup.select("div.gs-c-promo-body")
        for article in articles[:10]:  # Get top 10 articles
            title_tag = article.select_one("h3")
            link_tag = article.select_one("a.gs-c-promo-heading")
            img_tag = article.select_one("img")
            if title_tag and link_tag:
                news_list.append({
                    "title": title_tag.get_text(strip=True),
                    "link": "https://www.bbc.com" + link_tag['href'] if link_tag['href'].startswith("/") else link_tag['href'],
                    "image": img_tag['src'] if img_tag else None
                })
        return news_list
    except Exception as e:
        print(f"Error scraping {url}: {e}")
        return []

# Scrape ESPN Latest news
def scrape_espn_latest():
    try:
        r = requests.get("https://www.espn.com")
        soup = BeautifulSoup(r.content, "html.parser")
        news_list = []
        articles = soup.select("section#news-feed article")  # ESPN selector
        for article in articles[:10]:
            title_tag = article.select_one("h1, h2, h3")
            link_tag = article.select_one("a")
            img_tag = article.select_one("img")
            if title_tag and link_tag:
                news_list.append({
                    "title": title_tag.get_text(strip=True),
                    "link": link_tag['href'] if link_tag['href'].startswith("http") else "https://www.espn.com" + link_tag['href'],
                    "image": img_tag['src'] if img_tag else None
                })
        return news_list
    except Exception as e:
        print(f"Error scraping ESPN: {e}")
        return []

@app.get("/")
def home():
    return {"message": "Backend is working!"}

@app.get("/api/news")
def get_news():
    sports_news = {
        "Football": scrape_bbc_sport("https://www.bbc.com/sport/football"),
        "Cricket": scrape_bbc_sport("https://www.bbc.com/sport/cricket"),
        "Tennis": scrape_bbc_sport("https://www.bbc.com/sport/tennis"),
        "Basketball": scrape_bbc_sport("https://www.bbc.com/sport/basketball"),
        "Latest": scrape_espn_latest()
    }
    return JSONResponse(content=sports_news)
