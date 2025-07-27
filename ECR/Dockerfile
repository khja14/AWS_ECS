# Use the official Python image from Docker Hub
FROM python:3.11-slim

# Set the working directory
WORKDIR /app

# Copy application code and requirements
COPY app/requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY app/ ./

# Expose the port Flask will run on
EXPOSE 5000

# Run the Flask app
CMD ["python", "main.py"]