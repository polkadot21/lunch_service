# Dockerfile
FROM python:3.10-slim

WORKDIR /app
COPY requirements.txt /app/
RUN pip install -r requirements.txt
COPY . /app/

# Copy the Python script to wait for PostgreSQL
COPY wait_for_postgres.py /app/

# Add entrypoint script
COPY entrypoint.sh /app/
ENTRYPOINT ["sh", "-c", "/app/entrypoint.sh"]

EXPOSE 8000