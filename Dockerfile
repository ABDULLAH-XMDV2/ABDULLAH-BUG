# Dockerfile - For Railway/Render
FROM python:3.10-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application
COPY . .

# Create payloads directory
RUN mkdir -p payloads

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV BOT_TOKEN=${BOT_TOKEN}

# Start command
CMD ["python3", "main.py"]