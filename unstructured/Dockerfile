FROM unstructuredio/unstructured:0.14.8

CMD ["python3", "app.py"]

RUN mkdir -p /var/
WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY app.py /app/app.py
