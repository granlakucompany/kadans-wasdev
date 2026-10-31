# ==============================================================================
# KADANS WASDEV VIDEO ENGINE — Official Cloud & Serverless Dockerfile
# Konpatib ak: AWS Lambda (Container Image), Google Cloud Run, Modal, RunPod, Docker
# ==============================================================================

FROM python:3.12-slim-bookworm

ENV DEBIAN_FRONTEND=noninteractive \
    PYTHONUNBUFFERED=1 \
    KADANS_CHROME=/usr/bin/chromium \
    KADANS_WORKERS=4 \
    PORT=8080

# 1. Enstale Chromium headless, FFmpeg, ak Polis karaktè yo
RUN apt-get update && apt-get install -y --no-install-recommends \
    chromium \
    ffmpeg \
    fonts-freefont-ttf \
    fonts-liberation \
    fonts-dejavu-core \
    fonts-noto-color-emoji \
    ca-certificates \
    curl \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# 2. Kopye fichye pakè Kadans yo
COPY pyproject.toml /app/
COPY kadans /app/kadans
COPY README.md LICENSE /app/

# 3. Enstale depandans Python yo
RUN pip install --no-cache-dir -e .

# 4. Port pou sèvè nwaj (Cloud Run / AWS Lambda Web Adapter)
EXPOSE 8080

# 5. Entrypoint
ENTRYPOINT ["python3", "-m", "kadans"]
CMD ["server", "--port", "8080", "--host", "0.0.0.0"]
