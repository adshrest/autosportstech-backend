import random
from datetime import datetime

# Simple keyword sets for free generation
SOCCER_TEAMS = ["Barcelona", "Real Madrid", "Manchester United", "Liverpool", "Arsenal", "Chelsea", "Bayern Munich", "PSG"]
CRICKET_TEAMS = ["India", "Australia", "England", "Pakistan", "Sri Lanka", "Bangladesh", "South Africa", "New Zealand"]

SOCCER_EVENTS = [
    "defeated", "drew against", "lost to", "crushed", "battled", "outclassed", "fought hard against"
]
CRICKET_EVENTS = [
    "won against", "lost to", "tied with", "dominated", "clinched victory over", "suffered defeat from"
]

def generate_soccer_news():
    team1, team2 = random.sample(SOCCER_TEAMS, 2)
    event = random.choice(SOCCER_EVENTS)
    score1, score2 = random.randint(0, 4), random.randint(0, 4)
    headline = f"{team1} {event} {team2} ({score1}-{score2})"
    content = f"In a thrilling soccer match, {team1} {event} {team2} with a final score of {score1}-{score2}. The fans witnessed exciting gameplay and outstanding performances."
    return {"sport": "soccer", "headline": headline, "content": content, "date": datetime.now().strftime("%Y-%m-%d")}

def generate_cricket_news():
    team1, team2 = random.sample(CRICKET_TEAMS, 2)
    event = random.choice(CRICKET_EVENTS)
    runs1, runs2 = random.randint(150, 350), random.randint(150, 350)
    headline = f"{team1} {event} {team2} by {abs(runs1 - runs2)} runs"
    content = f"{team1} {event} {team2} in a high-scoring cricket clash, setting a total of {runs1} runs. {team2} replied with {runs2} runs."
    return {"sport": "cricket", "headline": headline, "content": content, "date": datetime.now().strftime("%Y-%m-%d")}

def generate_daily_news():
    # Generate 3 soccer + 3 cricket news items daily
    news_list = [generate_soccer_news() for _ in range(3)] + [generate_cricket_news() for _ in range(3)]
    random.shuffle(news_list)
    return news_list
