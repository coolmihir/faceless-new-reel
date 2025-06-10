# Use an official Python image
FROM python:3.10-slim

# Install build dependencies (now includes fonts)
RUN apt-get update && \
    apt-get install -y gcc ffmpeg imagemagick fonts-freefont-ttf libsm6 libxext6 libgl1 libglib2.0-0 \
    libjpeg-dev zlib1g-dev && \
    apt-get clean

# Optional: Fix ImageMagick policy issues (uncomment if needed)
RUN sed -i 's/none/read|write/g' /etc/ImageMagick-6/policy.xml || true

WORKDIR /app
COPY . /app

RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
