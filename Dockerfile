FROM python:3.11-slim

LABEL maintainer="moabukar"
LABEL description="MockOps - Master Your Next DevOps Interview"
LABEL version="1.2.0"
LABEL org.opencontainers.image.source="https://github.com/moabukar/devops-interview-prep"
LABEL org.opencontainers.image.documentation="https://github.com/moabukar/devops-interview-prep/blob/main/README.md"
LABEL org.opencontainers.image.licenses="MIT"

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

WORKDIR /app

RUN apt-get update && apt-get install -y \
    --no-install-recommends \
    curl \
    git \
    && rm -rf /var/lib/apt/lists/* \
    && apt-get clean

# create non-root user early
RUN useradd --create-home --shell /bin/bash --uid 1000 devops-interviewer

# copy only the requirements file that exists
COPY requirements.txt ./

RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

COPY src/ src/
COPY data/ data/
COPY pyproject.toml ./
COPY setup.py ./


RUN pip install --no-cache-dir -e .

RUN mkdir -p /home/devops-interviewer/.mockops && \
    chown -R devops-interviewer:devops-interviewer /app /home/devops-interviewer

USER devops-interviewer

WORKDIR /home/devops-interviewer

HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD mockops --version || exit 1

ENTRYPOINT ["mockops"]
CMD ["--help"]