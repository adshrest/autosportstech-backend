from fastapi import FastAPI
from app.news_generator import generate_daily_news

app = FastAPI()

@app.get("/")
def home():
    return {"message": "Backend is working!"}

@app.get("/api/news")
def get_news():
    return generate_daily_news()
