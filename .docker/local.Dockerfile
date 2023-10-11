FROM python:3.11.4-slim-bullseye

RUN python --version

COPY . /app/
WORKDIR /app

# OS dependencies
RUN apt-get update && apt-get install -y libpq-dev gcc

# Install Python dependencies
RUN pip install -U pip && pip install -r requirements.txt

# Install Prometheus
RUN apt-get install -y prometheus


EXPOSE 8080
EXPOSE 9090