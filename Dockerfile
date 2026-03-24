FROM python:3.11-slim

WORKDIR /app

COPY assistant_platform /app/assistant_platform
COPY README.md /app/README.md

RUN pip install --no-cache-dir --upgrade pip setuptools wheel
RUN pip install --no-cache-dir \
    fastapi>=0.115.0 \
    uvicorn>=0.30.0 \
    pydantic>=2.8.0 \
    pyyaml>=6.0.2 \
    python-dateutil>=2.9.0 \
    torch \
    transformers \
    peft \
    datasets

ENV PYTHONPATH=/app
ENV PORT=8080

CMD ["sh", "-c", "uvicorn assistant_platform.api.app:app --host 0.0.0.0 --port ${PORT}"]
