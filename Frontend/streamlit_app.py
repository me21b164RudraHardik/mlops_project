import streamlit as st
import psycopg2
from datetime import date
import pandas as pd

# Database config
DB_CONFIG = {
    'host': 'localhost',
    'port': 5432,
    'database': 'articles_db',
    'user': 'postgres',
    'password': 'admin'
}

def get_today_result():
    conn = psycopg2.connect(**DB_CONFIG)
    cursor = conn.cursor()
    cursor.execute("SELECT date, title, summary, vader_sentiment, market_trend FROM results WHERE date = %s", (date.today(),))
    row = cursor.fetchone()
    cursor.close()
    conn.close()
    return row

# Streamlit UI
st.set_page_config(page_title="Market Summary", layout="centered")

st.markdown(
    """
    <style>
    .big-title {
        font-size: 30px !important;
        font-weight: bold;
        text-align: center;
        margin-top: 20px;
    }
    .summary-text {
        font-size: 18px;
        text-align: justify;
        padding: 10px;
        background-color: #f8f9fa;
        border-radius: 10px;
        color: #155724;
    }
    .score-box {
        font-size: 24px;
        text-align: center;
        padding: 15px;
        border-radius: 12px;
        margin-top: 20px;
    }
    .positive {
        background-color: #d4edda;
        color: #155724;
    }
    .negative {
        background-color: #f8d7da;
        color: #721c24;
    }
    </style>
    """, unsafe_allow_html=True
)

# Fetch today's data
result = get_today_result()

if result:
    result_date, title, summary, vader_score, market_trend = result

    # Title
    st.markdown(f'<div class="big-title">{title}</div>', unsafe_allow_html=True)

    # Summary
    st.markdown('<h4 style="margin-top: 30px;">📝 Summary of Today\'s Market News</h4>', unsafe_allow_html=True)
    st.markdown(f'<div class="summary-text">{summary}</div>', unsafe_allow_html=True)

    # Market Trend Indicator
    trend_class = 'positive' if market_trend == "Positive" else 'negative'
    st.markdown(f'<div class="score-box {trend_class}">📈 Market Trend: <b>{market_trend}</b></div>', unsafe_allow_html=True)

    # Sentiment score
    st.markdown(f'<div class="score-box" style="background-color:#e2e3e5; color:#383d41;">Vader Sentiment Score: <b>{vader_score:.2f}</b></div>', unsafe_allow_html=True)

else:
    st.warning("No analysis available for today. Please run the pipeline or try again later.")
