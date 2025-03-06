# 使用 Python 官方映像檔
FROM python:3.11

# 設定工作目錄
WORKDIR /app

# 複製需求檔案並安裝
COPY app/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install pillow open-clip-torch
RUN pip install ollama
RUN pip install -U google-generativeai
RUN pip install fastapi uvicorn
RUN pip install Pillow
RUN pip install -q -U google-genai
RUN pip install python-multipart

# 複製應用程式程式碼
COPY app /app

# 啟動 FastAPI 伺服器
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
# CMD ["python3", "/app/main.py"]
