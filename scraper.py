import requests
from bs4 import BeautifulSoup
import pandas as pd
from tqdm import tqdm
import time

BASE_URL = "https://www.lexaloffle.com/bbs/?cat=7#sub=2"
HEADERS = {"User-Agent": "Mozilla/5.0"}

games = []

def get_soup(url):
    try:
        res = requests.get(url, headers=HEADERS, timeout=10)
        return BeautifulSoup(res.text, "html.parser")
    except:
        return None

# ✅ STEP 1: Get REAL game links
def get_game_links():
    soup = get_soup(BASE_URL)
    links = []

    for a in soup.select("a[href*='tid']"):
        href = a.get("href")
        if href and "tid=" in href:
            full = "https://www.lexaloffle.com" + href
            links.append(full)

    return list(set(links))[:100]

# ✅ STEP 2: Extract proper data
def extract_game(url):
    soup = get_soup(url)
    if not soup:
        return None

    try:
        # Title
        title_tag = soup.find("title")
        name = title_tag.text.split("::")[0].strip() if title_tag else ""

        # Author
        author_tag = soup.select_one("a[href*='uid']")
        author = author_tag.text.strip() if author_tag else ""

        # Artwork
        img_tag = soup.select_one("img[src*='bbs']")
        artwork = img_tag["src"] if img_tag else ""

        # Description
        desc_tag = soup.select_one("meta[name='description']")
        description = desc_tag["content"] if desc_tag else ""

        # Likes (approx)
        likes = soup.text.count("❤️")

        # Code (if exists)
        code_tag = soup.find("code")
        game_code = code_tag.text[:300] if code_tag else ""

        # Comments
        comments = soup.select(".post")[:5]
        top_comments = [c.text.strip()[:100] for c in comments]

        return {
            "name": name,
            "author": author,
            "artwork": artwork,
            "game_code": game_code,
            "license": "N/A",
            "likes": likes,
            "description": description,
            "top_comments": " | ".join(top_comments)
        }

    except:
        return None

def main():
    links = get_game_links()

    for link in tqdm(links):
        data = extract_game(link)
        if data:
            games.append(data)
        time.sleep(1)

    df = pd.DataFrame(games)
    df.to_csv("games_dataset.csv", index=False)
    print("✅ Dataset improved and saved!")

if __name__ == "__main__":
    main()
