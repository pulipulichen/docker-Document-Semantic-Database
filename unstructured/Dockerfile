FROM unstructuredio/unstructured:0.14.8

RUN mkdir -p /var/
WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install tiktoken==0.9.0

CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8080", "--reload"]

COPY app.py /app/app.py
