from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from bs4 import BeautifulSoup
import requests
import datetime

app = FastAPI()

# Allow frontend to access backend
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

SPORT_SITES = {
    "Football": "https://www.espn.com/soccer/",
    "Cricket": "https://www.espncricinfo.com/",
    "Basketball": "https://www.espn.com/nba/",
    "Tennis": "https://www.espn.com/tennis/"
}

@app.get("/")
def home():
    return {"message": "Backend is working!"}

@app.get("/api/news")
def get_news():
    news_data = {}
    for sport, url in SPORT_SITES.items():
        try:
            r = requests.get(url, headers={"User-Agent": "Mozilla/5.0"})
            soup = BeautifulSoup(r.text, "html.parser")
            
            # Collect top 5 headlines
            items = []
            articles = soup.find_all("a", limit=10)  # take first 10 links
            for a in articles:
                title = a.get_text().strip()
                link = a.get("href")
                if link and not link.startswith("http"):
                    # make full URL if relative
                    link = url.rstrip("/") + "/" + link.lstrip("/")
                if title and link:
                    items.append({
                        "title": title,
                        "link": link,
                        "image": None,  # some sites don't provide images in simple scrape
                        "sport": sport
                    })
                if len(items) >= 5:
                    break
            news_data[sport] = items
        except Exception as e:
            news_data[sport] = [{"title": f"Could not fetch {sport} news", "link": "", "image": None, "sport": sport}]
    
    # Minor sports go in "Others"
    news_data["Others"] = [{"title": "No minor sports news yet", "link": "", "image": None, "sport": "Others"}]
    news_data["last_updated"] = datetime.datetime.utcnow().isoformat()
    return news_data
