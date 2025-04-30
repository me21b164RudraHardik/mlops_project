# main.py

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import psycopg2
from datetime import datetime
import json
from scrape_articles import scrape_top_articles, insert_into_db
from data_analysis import analyze_and_store
from prometheus_fastapi_instrumentator import Instrumentator

app = FastAPI()

# Add Prometheus metrics endpoint
Instrumentator().instrument(app).expose(app, include_in_schema=False, endpoint="/metrics")

# DB config
DB_CONFIG = {
    "host": "postgres",
    "port": 5432,
    "database": "articles_db",
    "user": "postgres",
    "password": "admin"
}

# ----------- ROUTES -----------

@app.post("/scrape/")
def run_scraper():
    today = datetime.today().date()
    try:
        articles = scrape_top_articles(limit=10)
        insert_into_db(today, articles)
        return {"message": f"Scraped and stored top 10 articles for {today}"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Scraper failed: {str(e)}")


@app.post("/analyze/")
def run_analysis():
    try:
        analyze_and_store()
        return {"message": "Analysis completed and results saved to DB."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Analysis failed: {str(e)}")


@app.get("/results/{date}")
def get_result(date: str):
    """Return market prediction and summary for given date (YYYY-MM-DD)"""
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        cursor = conn.cursor()
        cursor.execute("SELECT date, title, summary, vader_sentiment, market_trend FROM results WHERE date = %s", (date,))
        row = cursor.fetchone()
        cursor.close()
        conn.close()

        if row:
            return {
                "date": row[0],
                "title": row[1],
                "summary": row[2],
                "vader_sentiment": row[3],
                "market_trend": row[4]
            }
        else:
            raise HTTPException(status_code=404, detail=f"No result found for date {date}")

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
    
