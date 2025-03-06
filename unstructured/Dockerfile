FROM unstructuredio/unstructured:0.14.8

CMD ["python3", "app.py"]

RUN mkdir -p /var/
WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
RUN pip install paddlepaddle
RUN pip install unstructured_paddleocr
RUN pip install hanzidentifier
RUN pip install opencc-python-reimplemented


COPY app.py /app/app.py
