# Dockerfile - Railway/Render
FROM python:3.10-slim

WORKDIR /app

# Install dependencies with timeout
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt --timeout=100

# Copy application
COPY . .

# Create payloads directory
RUN mkdir -p payloads

# Set environment
ENV PYTHONUNBUFFERED=1

# Start command
CMD ["python3", "main.py"]
