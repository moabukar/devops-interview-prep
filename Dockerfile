FROM python:3.11-alpine

LABEL maintainer="moabukar"
LABEL description="MockOps - Master Your Next DevOps Interview"
LABEL version="1.2.0"
LABEL org.opencontainers.image.source="https://github.com/moabukar/mockops"
LABEL org.opencontainers.image.licenses="MIT"

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1

WORKDIR /app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY src/ src/
COPY data/ data/
COPY pyproject.toml setup.py ./
RUN pip install --no-cache-dir . && \
    pip uninstall -y pip setuptools wheel 2>/dev/null; \
    rm -rf /usr/local/lib/python3.11/site-packages/pip \
           /usr/local/lib/python3.11/site-packages/setuptools \
           /usr/local/lib/python3.11/site-packages/wheel \
           /usr/local/lib/python3.11/site-packages/pkg_resources

RUN adduser -D -u 1000 mockops && \
    mkdir -p /home/mockops/.mockops && \
    chown -R mockops:mockops /home/mockops

USER mockops
WORKDIR /app

HEALTHCHECK --interval=60s --timeout=5s --retries=2 \
    CMD mockops --version || exit 1

ENTRYPOINT ["mockops"]
CMD ["--help"]
