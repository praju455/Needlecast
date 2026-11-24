FROM python:3.13-slim
WORKDIR /app
ENV PYTHONUNBUFFERED=1 PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=/app/ml/src
COPY ml/requirements/base.txt ml/requirements/base.txt
COPY backend/requirements.txt backend/requirements.txt
RUN pip install --no-cache-dir -r ml/requirements/base.txt -r backend/requirements.txt \
    && useradd --create-home --uid 10001 needlecast
COPY VERSION ./
COPY ml/src ml/src
COPY backend/app backend/app
USER needlecast
EXPOSE 8000
HEALTHCHECK --interval=10s --timeout=3s --retries=4 CMD ["python", "-c", "import urllib.request; urllib.request.urlopen('http://127.0.0.1:8000/health', timeout=2)"]
CMD ["python", "-m", "uvicorn", "backend.app.main:app", "--host", "0.0.0.0", "--port", "8000", "--no-access-log"]
