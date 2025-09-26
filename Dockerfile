FROM apache/airflow:3.1.0
COPY requirements.txt .
RUN pip install -r requirements.txt