FROM python:3.10-slim

WORKDIR /app

COPY backend/ /app/
RUN pip install fastapi uvicorn psycopg2-binary prometheus-fastapi-instrumentator

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
