import psycopg2
import json
import pandas as pd
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from transformers import pipeline
from datetime import datetime

# Database connection settings
DB_CONFIG = {
    'host': 'localhost',
    'dbname': 'articles_db',
    'user': 'postgres',
    'password': 'admin'
}

# Function to summarize text using transformers
def summarize_content(content):
    summarizer = pipeline("summarization", model="facebook/bart-large-cnn")
    try:
        summary = summarizer(content, max_length=200, min_length=50, do_sample=False)
        return summary[0]['summary_text']
    except Exception as e:
        print(f"Error summarizing content: {e}")
        return "Summary generation failed"

# Fetch from daily_articles table
def fetch_articles_from_db():
    conn = psycopg2.connect(**DB_CONFIG)
    cursor = conn.cursor()

    cursor.execute("SELECT date, articles FROM daily_articles ORDER BY date")
    rows = cursor.fetchall()
    cursor.close()
    conn.close()

    data = []
    for row in rows:
        date = row[0]
        articles = row[1]

        # Combine all article content into one string
        combined_content = "\n\n".join(article.get("content", "") for article in articles if article.get("content"))

        # Summarize content
        summary = summarize_content(combined_content)

        # Title for the day
        title = f"Market Summary for {date.strftime('%Y-%m-%d')}"

        data.append({
            "date": date,
            "title": title,
            "summary": summary
        })

    return pd.DataFrame(data)

# Analyze sentiment and trend
def analyze_and_store():
    df = fetch_articles_from_db()
    if df.empty:
        print("No data found in daily_articles.")
        return

    # Sentiment Analysis
    analyzer = SentimentIntensityAnalyzer()
    df["vader_sentiment"] = df["summary"].apply(lambda x: analyzer.polarity_scores(x)["compound"])
    df["market_trend"] = df["vader_sentiment"].apply(lambda x: "Positive" if x > 0 else "Negative")

    # Save to results table
    conn = psycopg2.connect(**DB_CONFIG)
    cursor = conn.cursor()

    for _, row in df.iterrows():
        try:
            cursor.execute("""
                INSERT INTO results (date, title, summary, vader_sentiment, market_trend)
                VALUES (%s, %s, %s, %s, %s)
                ON CONFLICT (date) DO UPDATE SET
                    title = EXCLUDED.title,
                    summary = EXCLUDED.summary,
                    vader_sentiment = EXCLUDED.vader_sentiment,
                    market_trend = EXCLUDED.market_trend;
            """, (row["date"], row["title"], row["summary"], row["vader_sentiment"], row["market_trend"]))
        except Exception as e:
            print(f"Failed to insert for {row['date']}: {e}")

    conn.commit()
    cursor.close()
    conn.close()
    print("Results inserted into `results` table.")

if __name__ == "__main__":
    analyze_and_store()
