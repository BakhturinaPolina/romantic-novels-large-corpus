FROM nvidia/cuda:12.8.1-cudnn-runtime-ubuntu24.04

ENV DEBIAN_FRONTEND=noninteractive \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    VIRTUAL_ENV=/opt/venv \
    PATH=/opt/venv/bin:$PATH

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    python3 \
    python3-dev \
    python3-pip \
    python3-venv \
    build-essential \
    git \
    curl \
    ca-certificates \
    && rm -rf /var/lib/apt/lists/*

RUN python3 -m venv "$VIRTUAL_ENV" \
    && python -m pip install --upgrade pip setuptools wheel

# Install Python dependencies first for better Docker layer caching.
COPY requirements.txt requirements-venv.txt ./
RUN python -m pip install -r requirements.txt \
    && python -m pip install --no-deps octis==1.14.0 \
    && python -m pip install tf-keras \
    && python -m spacy download en_core_web_sm

COPY src ./src
COPY configs ./configs
COPY Makefile ./
COPY .env.example ./
COPY README.md ./

CMD ["python", "-m", "src.stage03_train.cli", "tune", "--config", "configs/train.yaml"]
