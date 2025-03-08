# 使用 Python 官方映像檔
FROM python:3.11

# 設定工作目錄
WORKDIR /app

# 複製需求檔案並安裝
COPY app/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

RUN apt update
RUN apt install -y libgl1-mesa-glx

ENV UVICORN_WORKERS=8

# 啟動 FastAPI 伺服器
# CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "${UVICORN_WORKERS}"]
# CMD ["python3", "ollama_vision.py"]
