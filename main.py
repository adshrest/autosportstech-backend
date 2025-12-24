from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.news_generator import get_all_news

app = FastAPI()

origins = [
    "https://sportsread.netlify.app",
    "http://localhost:8080"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_methods=["*"],
    allow_headers=["*"]
)

@app.get("/")
def root():
    return {"status": "Backend running"}

@app.get("/api/news")
def news():
    return get_all_news()
