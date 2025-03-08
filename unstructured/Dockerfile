FROM unstructuredio/unstructured:0.14.8

RUN mkdir -p /var/
WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

ENV UVICORN_WORKERS=8

# CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8080", "--reload"]
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "${UVICORN_WORKERS}"]

COPY app.py /app/app.py
