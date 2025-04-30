# scripts/scrape_articles.py

import requests
from bs4 import BeautifulSoup
import psycopg2
import json
from datetime import datetime
import re

DB_CONFIG = {
    "host": "localhost",
    "port": 5432,
    "database": "articles_db",
    "user": "postgres",
    "password": "admin"
}

def clean_text(text):
    text = re.sub(r'\s+', ' ', text)               # Remove extra spaces/newlines
    text = re.sub(r'[^\w\s.,!?-]', '', text)       # Remove unwanted characters
    return text.strip()

def fetch_article_content(url):
    try:
        response = requests.get(url, timeout=5)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')

        # Extract content from divs (MoneyControl uses multiple class names)
        container = soup.find('div', class_='content_wrapper') or soup.find('div', class_='article_content') or soup.find('div', {'class': re.compile('.*article.*')})
        if not container:
            return "Content not found"

        paragraphs = container.find_all('p')
        content = " ".join(p.get_text() for p in paragraphs if p.get_text())
        return clean_text(content)
    except Exception as e:
        print(f"❌ Failed to fetch article content from {url}: {e}")
        return "Error fetching content"

def scrape_top_articles(limit=10):
    url = "https://www.moneycontrol.com/news/business/markets/"
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        raise Exception("Failed to load MoneyControl page")

    soup = BeautifulSoup(response.content, "html.parser")
    articles = soup.find_all('li', class_="clearfix")

    results = []
    count = 0

    for article in articles:
        if count >= limit:
            break
        title_tag = article.find('h2')
        if not title_tag:
            continue

        title = clean_text(title_tag.get_text(strip=True))
        link_tag = title_tag.find('a')
        link = link_tag['href'] if link_tag else ''
        if not link or not title:
            continue

        content = fetch_article_content(link)
        results.append({
            "title": title,
            "link": link,
            "content": content
        })
        count += 1

    return results

def insert_into_db(date, articles):
    conn = psycopg2.connect(**DB_CONFIG)
    cursor = conn.cursor()

    insert_query = """
    INSERT INTO daily_articles (date, articles)
    VALUES (%s, %s)
    """
    cursor.execute(insert_query, (date, json.dumps(articles)))
    conn.commit()
    cursor.close()
    conn.close()

if __name__ == "__main__":
    today = datetime.today().date()
    articles = scrape_top_articles(limit=10)
    insert_into_db(today, articles)
    print(f"Inserted Top 10 articles for {today} with full content.")
