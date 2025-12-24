import requests
from bs4 import BeautifulSoup

def scrape_bbc_sport(category_url, limit=5):
    """Scrapes BBC Sport for a category and returns list of dicts with title, link, image."""
    news = []
    try:
        res = requests.get(category_url)
        soup = BeautifulSoup(res.text, "html.parser")
        articles = soup.select("a.gs-c-promo-heading")[:limit]
        for a in articles:
            title = a.get_text(strip=True)
            link = a['href']
            if not link.startswith("http"):
                link = "https://www.bbc.com" + link
            # Find image
            parent = a.find_parent("div", class_="gs-c-promo")
            img_tag = parent.find("img") if parent else None
            image = img_tag["src"] if img_tag and img_tag.has_attr("src") else ""
            news.append({"title": title, "link": link, "image": image})
    except Exception as e:
        print(f"Error scraping BBC {category_url}: {e}")
    return news

def scrape_espn_latest(limit=5):
    """Scrape ESPN latest news (general)"""
    news = []
    try:
        url = "https://www.espn.com/espn/latestnews"
        res = requests.get(url)
        soup = BeautifulSoup(res.text, "html.parser")
        articles = soup.select("section.contentItem")[:limit]
        for art in articles:
            title_tag = art.find("h1") or art.find("h2") or art.find("a")
            link_tag = art.find("a", href=True)
            img_tag = art.find("img")
            if title_tag and link_tag:
                title = title_tag.get_text(strip=True)
                link = link_tag['href']
                if not link.startswith("http"):
                    link = "https://www.espn.com" + link
                image = img_tag['src'] if img_tag and img_tag.has_attr("src") else ""
                news.append({"title": title, "link": link, "image": image})
    except Exception as e:
        print("Error scraping ESPN latest:", e)
    return news

def generate_all_sports_news():
    """Return grouped news by sport"""
    sports_news = {
        "Football": scrape_bbc_sport("https://www.bbc.com/sport/football"),
        "Cricket": scrape_bbc_sport("https://www.bbc.com/sport/cricket"),
        "Tennis": scrape_bbc_sport("https://www.bbc.com/sport/tennis"),
        "Basketball": scrape_bbc_sport("https://www.bbc.com/sport/basketball"),
        "Latest": scrape_espn_latest()
    }
    return sports_news
