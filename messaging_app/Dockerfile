# Use python:3.10 as base image
FROM python:3.10

# Prevent Python from writing pyc files
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set work directory
WORKDIR /app

# Copy and install requirements
COPY requirements.txt .
RUN pip install -r requirements.txt

# Copy project
COPY . .

# Expose port 8000
 

# Start server
 
docker run -d -p 8000:8000 --name test-container test-app

