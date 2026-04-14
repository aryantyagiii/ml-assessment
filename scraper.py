import requests
from bs4 import BeautifulSoup
import pandas as pd
from tqdm import tqdm
import time

BASE_URL = "https://www.lexaloffle.com/bbs/?cat=7#sub=2"  # example Pico-8 games

headers = {
    "User-Agent": "Mozilla/5.0"
}

games = []

def get_soup(url):
    try:
        res = requests.get(url, headers=headers, timeout=10)
        return BeautifulSoup(res.text, "html.parser")
    except:
        return None

def scrape_game_links():
    soup = get_soup(BASE_URL)
    if not soup:
        return []

    links = []
    for a in soup.select("a"):
        href = a.get("href")
        if href and "tid=" in href:
            full_url = "https://www.lexaloffle.com" + href
            links.append(full_url)

    return list(set(links))[:100]

def extract_game(url):
    soup = get_soup(url)
    if not soup:
        return None

    try:
        name = soup.select_one("title")
        name = name.text.strip() if name else ""

        author = soup.select_one("a[href*='uid']")
        author = author.text.strip() if author else ""

        artwork = soup.select_one("img")
        artwork = artwork["src"] if artwork else ""

        code = soup.select_one("code")
        code = code.text[:500] if code else ""  # limit size

        description = soup.select_one("meta[name='description']")
        description = description["content"] if description else ""

        likes = soup.text.count("❤️")  # fallback

        comments = soup.select(".post")[:5]
        top_comments = [c.text.strip()[:100] for c in comments]

        return {
            "name": name,
            "author": author,
            "artwork": artwork,
            "game_code": code,
            "license": "N/A",
            "likes": likes,
            "description": description,
            "top_comments": " | ".join(top_comments)
        }

    except:
        return None


def main():
    links = scrape_game_links()

    for link in tqdm(links):
        data = extract_game(link)
        if data:
            games.append(data)
        time.sleep(1)  # avoid blocking

    df = pd.DataFrame(games)
    df.to_csv("games_dataset.csv", index=False)
    print("✅ Dataset ready")

if __name__ == "__main__":
    main()