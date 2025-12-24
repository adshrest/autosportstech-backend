from bs4 import BeautifulSoup
import requests

SPORT_SOURCES = {
    "Football": "https://www.espn.com/nfl/",
    "Basketball": "https://www.espn.com/nba/",
    "Cricket": "https://www.espncricinfo.com/",
    "Tennis": "https://www.espn.com/tennis/",
    "Soccer": "https://www.espn.com/soccer/"
}

def generate_daily_news():
    news_items = []

    for sport, url in SPORT_SOURCES.items():
        try:
            r = requests.get(url, timeout=10)
            soup = BeautifulSoup(r.text, "html.parser")
            
            # Grab first 3 headlines (adjust selectors based on the site)
            headlines = soup.select("section h1, section h2, section h3")[:3]
            
            for h in headlines:
                title = h.get_text(strip=True)
                link_tag = h.find_parent("a")
                news_url = link_tag["href"] if link_tag else url
                news_items.append({
                    "title": title,
                    "content": "",  # optional summary if available
                    "url": news_url if news_url.startswith("http") else f"https://www.espn.com{news_url}",
                    "image": "",  # optional, add image scraping if desired
                    "sport": sport
                })
        except Exception as e:
            print(f"Error fetching {sport}: {e}")
            continue

    return news_items
