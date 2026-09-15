FROM nvidia/cuda:12.1.1-runtime-ubuntu22.04

# Set non-interactive environment and port definitions
ENV PYTHONUNBUFFERED=1 \
    DEBIAN_FRONTEND=noninteractive \
    PORT=8080 \
    GRADIO_SERVER_NAME="0.0.0.0" \
    GRADIO_SERVER_PORT=8080 \
    GRADIO_ALLOW_FLAGGING=never

WORKDIR /app

# Install system dependencies for audio synthesis, speech recognition, and Python C-extensions
RUN apt-get update && apt-get install -y --no-install-recommends \
    python3.10 \
    python3-pip \
    git \
    ffmpeg \
    libsndfile1 \
    portaudio19-dev \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip3 install --no-cache-dir -r requirements.txt

# Copy application source code
COPY . .

# Expose server port
EXPOSE 8080

# Launch Gradio Command Center with unbuffered output
CMD ["python3", "-u", "dashboard/app.py"]
