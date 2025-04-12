FROM ubuntu:20.04
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip \
    python3-dev \
    portaudio19-dev \
    libsndfile1 \
    ffmpeg \
    libhdf5-dev \
    pkg-config \
    build-essential \
    && rm -rf /var/lib/apt/lists/*
RUN ln -s /usr/bin/python3 /usr/bin/python
RUN useradd -m -u 1000 appuser
WORKDIR /app
COPY requirements.txt .
RUN python -m pip install --upgrade pip
RUN pip3 install --no-cache-dir -r requirements.txt
COPY . .
RUN mkdir -p static/uploads && \
    chown -R appuser:appuser /app && \
    chmod -R 755 /app
USER appuser
EXPOSE 8000
# CMD ["python", "-m", "flask", "run", "--host=0.0.0.0"]
CMD ["python3", "main.py"]