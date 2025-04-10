# Use official Python image
FROM python:3.11-slim

# Set working directory inside container
WORKDIR /app

# Copy everything to container
COPY . .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Default command to run app
CMD ["python", "app/main.py"]
