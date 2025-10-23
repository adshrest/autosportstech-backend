from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.news_generator import generate_daily_news

app = FastAPI()

# Allow frontend to access backend
origins = [
    "https://sportsread.netlify.app/",  # your frontend URL
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

@app.get("/")
def home():
    return {"message": "Backend is working!"}

@app.get("/api/news")
def get_news():
    return generate_daily_news()
