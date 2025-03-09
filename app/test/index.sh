# #!/bin/bash
#
# curl -X 'POST' \
#   'http://localhost:8000/index' \
#   -H 'accept: application/json' \
#   -H 'Content-Type: multipart/form-data' \
#   -F 'file=@02.webp' \
#   -F 'document=Hello World'
#

echo "傳送第一個"

curl -X 'POST' \
  'http://localhost:8889/index' \
  -H 'accept: application/json' \
  -H 'Content-Type: multipart/form-data' \
  -F 'document=abc' \
  -F 'metadata={"a":1,"b":2,"c":3}'

echo "傳送第二個"

curl -X 'POST' \
  'http://localhost:8889/index' \
  -H 'accept: application/json' \
  -H 'Content-Type: multipart/form-data' \
  -F 'document=def' \
  -F 'metadata={"a":1,"b":2,"c":3}'

echo "傳送第三個"

curl -X 'POST' \
  'http://localhost:8889/index' \
  -H 'accept: application/json' \
  -H 'Content-Type: multipart/form-data' \
  -F 'title=測試A' \
  -F 'file=@civitai.png'

echo "傳送第四個"

curl -X 'POST' \
  'http://localhost:8889/index' \
  -H 'accept: application/json' \
  -H 'Content-Type: multipart/form-data' \
  -F 'title=測試B' \
  -F 'file=@miku.png'
#
echo "傳送第五個"

curl -X 'POST' \
  'http://192.168.89.1:8889/index' \
  -H 'accept: application/json' \
  -H 'Content-Type: multipart/form-data' \
  -F 'title=1a_test' \
  -F 'download_url=https://image.civitai.com/xG1nkqKTMzGDvpLrqFT7WA/db1fd945-1ff4-4d63-8fa3-01f90fa492c4/original=true,quality=90/00037-2152714628.jpeg'

# # http://localhost:8000/knowledge_base/knowledge_base/item/abc/
