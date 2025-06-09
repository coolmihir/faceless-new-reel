# Use official Python image
FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Copy all files from the current folder into the container
COPY . .

# Install system dependencies for moviepy and whisper (ffmpeg etc.)
RUN apt-get update && \
    apt-get install -y ffmpeg libsm6 libxext6 && \
    rm -rf /var/lib/apt/lists/*

# Install Python dependencies (make sure requirements.txt includes moviepy)
RUN pip install --upgrade pip && pip install -r requirements.txt

# Set environment port (Railway uses this to expose your app)
ENV PORT=8000

# Command to run your FastAPI app with Uvicorn
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
