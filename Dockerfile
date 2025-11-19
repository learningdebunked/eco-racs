FROM python:3.11-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy source code
COPY src/ ./src/
COPY config/ ./config/

# Expose API port
EXPOSE 8000

# Run API server
CMD ["uvicorn", "cac.api.checkout_api:app", "--host", "0.0.0.0", "--port", "8000"]
