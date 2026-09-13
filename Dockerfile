FROM nvidia/cuda:12.1.1-runtime-ubuntu22.04

# Prevent interactive prompts during installation
ENV DEBIAN_FRONTEND=noninteractive

# Install System Dependencies & Python 3.11
RUN apt-get update && apt-get install -y \
    python3.11 \
    python3-pip \
    portaudio19-dev \
    ffmpeg \
    git \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copy application files
COPY . /app

# Upgrade pip and install Python packages
RUN python3.11 -m pip install --upgrade pip
RUN python3.11 -m pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu121
RUN python3.11 -m pip install -r requirements.txt || true
RUN python3.11 -m pip install gradio z3-solver elevenlabs speechrecognition reportlab jinja2 huggingface_hub

EXPOSE 7870

# Launch dashboard
CMD ["python3.11", "-B", "dashboard/app.py"]
