# Use an official Python image
FROM python:3.10-slim

# Install build dependencies for Pillow and MoviePy, **including ImageMagick**
RUN apt-get update && \
    apt-get install -y gcc ffmpeg imagemagick libsm6 libxext6 libgl1 libglib2.0-0 \
    libjpeg-dev zlib1g-dev && \
    apt-get clean

# Set working directory
WORKDIR /app

# Copy all files
COPY . /app

# Create virtualenv and install dependencies
RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Run the app
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
