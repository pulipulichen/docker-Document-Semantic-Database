import requests
import time

time.sleep(5)

url = "http://unstructured:8080/process"
file_path = "/app/test/example.pdf"

print('準備開始上傳')

with open(file_path, "rb") as file:
    files = {"file": file}
    headers = {"accept": "application/json"}
    
    response = requests.post(url, headers=headers, files=files)

# 打印回應結果
print(response.status_code)
print(response.json())  # 假設返回 JSON 格式的數據
