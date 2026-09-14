# ============================================================
# Dockerfile for WellVia
# ============================================================
# This file tells Google Cloud Run (or any Docker host) how
# to package and run your Flask app inside a container.
#
# You do NOT need to understand every line as a beginner —
# just know that this file makes deployment possible.
# ============================================================

# Start from an official lightweight Python image
FROM python:3.11-slim

# Set the working directory inside the container
WORKDIR /app

# Copy the requirements file first (for faster re-builds)
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the project files into the container
COPY . .

# Tell the container which port to expose
EXPOSE 8080

# Start the app using gunicorn (a production-ready web server)
# gunicorn is better than Flask's built-in server for real deployments
CMD ["gunicorn", "--bind", "0.0.0.0:8080", "--workers", "1", "--threads", "8", "app:app"]
