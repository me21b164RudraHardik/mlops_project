FROM python:3.10-slim

WORKDIR /app

COPY frontend/ /app/
RUN pip install streamlit psycopg2-binary pandas

EXPOSE 8501
CMD ["streamlit", "run", "streamlit_app.py", "--server.port=8501", "--server.address=0.0.0.0"]
