# **AI-Powered Market News Analysis and Visualization System**

## **1. Overview**

This project implements an end-to-end, modular, and automated pipeline that collects and analyzes Indian market news on a daily basis. The system scrapes articles from a trusted financial news source (MoneyControl), summarizes and analyzes their content using state-of-the-art Natural Language Processing (NLP) models, computes sentiment, predicts market trends, and stores the results. The processed outputs are served via RESTful APIs and visualized through a responsive web-based dashboard.

The solution integrates key MLOps components including orchestration (Airflow), observability (Prometheus and Grafana), scalable APIs (FastAPI), and an accessible frontend (Streamlit), while ensuring data persistence and auditability via PostgreSQL.

---

## **2. Key Features**

- Daily automated ingestion of top 10 market news articles from MoneyControl.
- Full-text extraction from each article using BeautifulSoup.
- Summarization of article content using a transformer-based NLP model (`facebook/bart-large-cnn`).
- Sentiment analysis using VADER sentiment analyzer.
- Market trend classification based on sentiment polarity.
- Centralized PostgreSQL storage for raw and processed data.
- RESTful API for triggering and accessing analysis outputs.
- Streamlit-based user interface for non-technical users.
- End-to-end monitoring via Prometheus and Grafana.
- Task orchestration and scheduling with Apache Airflow.

---

## **3. System Architecture**

The architecture consists of the following core layers:

- **Data Ingestion Layer**: Responsible for scraping top news articles from MoneyControl and storing them in raw format.
- **Processing and Analysis Layer**: Summarizes content and performs sentiment-based market trend prediction.
- **Storage Layer**: A PostgreSQL database stores raw and processed data in normalized relational tables.
- **Service Layer**: FastAPI exposes services to trigger pipelines and query results.
- **Presentation Layer**: Streamlit displays processed results to users.
- **Monitoring Layer**: Prometheus and Grafana monitor performance and health.
- **Orchestration Layer**: Airflow schedules and coordinates scraping and analysis tasks.

---

## **4. Technology Stack**

| Component           | Technology Used            |
|---------------------|-----------------------------|
| Web Scraping        | Python, Requests, BeautifulSoup |
| NLP Models          | Transformers (BART), VADER |
| API Framework       | FastAPI                    |
| Frontend Dashboard  | Streamlit                  |
| Orchestration       | Apache Airflow             |
| Storage             | PostgreSQL                 |
| Monitoring          | Prometheus, Grafana        |
| Deployment (optional) | Docker, Docker Compose  |

---

## **5. Folder Structure**

```
project/
├── Backend/
|   ├── scrape_articles.py           # Scraper for MoneyControl articles
|   ├── data_analysis.py             # Summarizer and sentiment analyzer
|   ├── main.py                      # FastAPI backend implementation
|   ├── streamlit_app.py             # Streamlit UI
|   ├── dags/
|   │   ├── scrape_articles_dag.py     # Airflow DAG for scraping
|   │   └── analyze_articles_dag.py    # Airflow DAG for analysis
|   ├── requirements.txt             # Project dependencies
|   ├── Dockerfile
├── Frontend/
|   ├── streamlit_app.py
|   ├── Dockerfile
├── Prometheus/
|   ├── prometheus.yml
├── docker-compose.yaml
├── README.md                    # Project documentation
```

---

## **6. Database Schema**

### Table: `daily_articles`
Stores raw scraped articles in JSON format.

| Field     | Type    | Description                          |
|-----------|---------|--------------------------------------|
| `date`    | DATE    | Date of ingestion (Primary Key)      |
| `articles`| JSON    | Array of articles with title, link, content |

### Table: `results`
Stores analysis output for each day.

| Field            | Type     | Description                        |
|------------------|----------|------------------------------------|
| `id`             | SERIAL   | Unique identifier                  |
| `date`           | DATE     | Date of analysis (Unique)          |
| `title`          | TEXT     | Title summarizing the market news |
| `summary`        | TEXT     | Consolidated summary of the day’s news |
| `vader_sentiment`| FLOAT    | Compound sentiment score (-1 to +1) |
| `market_trend`   | TEXT     | Classified market trend (Positive/Negative) |

---

## **7. Setup Instructions**

### Step 1: Clone the Repository
```bash
git clone https://github.com/yourusername/market-news-analysis.git
cd market-news-analysis
```

### Step 2: Create and Activate a Virtual Environment
```bash
python -m venv venv
source venv/bin/activate   # On Windows: venv\Scripts\activate
```

### Step 3: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 4: Set Up PostgreSQL
Create the required database and tables using:

```sql
CREATE DATABASE articles_db;

CREATE TABLE daily_articles (
    date DATE PRIMARY KEY,
    articles JSON
);

CREATE TABLE results (
    id SERIAL PRIMARY KEY,
    date DATE UNIQUE,
    title TEXT,
    summary TEXT,
    vader_sentiment FLOAT,
    market_trend TEXT
);
```

---

## **8. Running the Services**

### FastAPI (Backend API)
```bash
uvicorn main:app --reload
```
Access Swagger UI at: [http://localhost:8000/docs](http://localhost:8000/docs)

### Streamlit (Frontend Dashboard)
```bash
streamlit run streamlit_app.py
```
Access UI at: [http://localhost:8501](http://localhost:8501)

### Airflow (for automation)
```bash
airflow scheduler
airflow webserver
```
Ensure your DAGs are placed under the `dags/` directory.

---

## **9. API Endpoints**

| Method | Endpoint            | Description                              |
|--------|---------------------|------------------------------------------|
| POST   | `/scrape/`          | Triggers scraping of the latest articles |
| POST   | `/analyze/`         | Performs summarization and trend analysis|
| GET    | `/results/{date}`   | Fetches analysis result for a given date |

---

## **10. Monitoring Setup**

- Configure Prometheus to scrape metrics from FastAPI at `/metrics`.
- Use Grafana to visualize:
  - API usage
  - Server health (CPU, memory, disk IO)
  - Database performance
- Include exporters like `postgres_exporter` and `node_exporter` for infrastructure metrics.

---

## **11. Test Strategy**

Refer to the `Test Plan & Test Cases` document for:

- Functional tests (API responses, UI rendering)
- Database integrity tests
- Monitoring availability
- Edge case validation

---

## **12. User Instructions (Non-Technical)**

1. Open the dashboard at [http://localhost:8501](http://localhost:8501)
2. Review:
   - Daily headline (AI-generated)
   - Summary of market news
   - Sentiment score and trend prediction
3. If the data is missing or outdated, contact the system admin to:
   - Open the API portal at [http://localhost:8000/docs](http://localhost:8000/docs)
   - Trigger `/scrape` followed by `/analyze`
   - Refresh the dashboard page

---
