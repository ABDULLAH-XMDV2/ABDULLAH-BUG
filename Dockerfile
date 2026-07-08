# Dockerfile - Complete Fixed Version
FROM python:3.10-slim

WORKDIR /app

# Install system dependencies for sqlite3 (if needed)
RUN apt-get update && apt-get install -y \
    sqlite3 \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements
COPY requirements.txt .

# Install Python packages (NO sqlite3!)
RUN pip install --no-cache-dir -r requirements.txt --timeout=100

# Copy application
COPY . .

# Create directories
RUN mkdir -p payloads

# Set environment
ENV PYTHONUNBUFFERED=1

# Start command
CMD ["python3", "main.py"]
