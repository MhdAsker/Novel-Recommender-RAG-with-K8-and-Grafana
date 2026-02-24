## Parent image
FROM python:3.10-slim

## Essential environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

## Work directory inside the docker container
WORKDIR /app

## Installing system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

## Explicitly copy folders to ensure nothing is missed
COPY app ./app
COPY Novels_Data ./Novels_Data
COPY pipeline ./pipeline
COPY config ./config
COPY src ./src
COPY utils ./utils
COPY setup.py requirements.txt ./

## Install dependencies
RUN pip install --no-cache-dir -e .

# Used PORTS
EXPOSE 8501

# Run the app
CMD ["streamlit", "run", "app/app.py", "--server.port=8501", "--server.address=0.0.0.0", "--server.headless=true"]
