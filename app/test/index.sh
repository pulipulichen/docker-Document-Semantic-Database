#!/bin/bash

curl -X 'POST' \
  'http://localhost:8000/index' \
  -H 'accept: application/json' \
  -H 'Content-Type: multipart/form-data' \
  -F 'file=@02.webp' \
  -F 'document=Hello World'

# curl -X 'POST' \
#   'http://localhost:8000/index' \
#   -H 'accept: application/json' \
#   -H 'Content-Type: multipart/form-data' \
#   -F 'document=abc' \
#   -F 'metadata={"a":1,"b":2,"c":3}'

# curl -X 'POST' \
#   'http://localhost:8000/index' \
#   -H 'accept: application/json' \
#   -H 'Content-Type: multipart/form-data' \
#   -F 'file=@02.webp'

# curl -X 'POST' \
#   'http://localhost:8000/index' \
#   -H 'accept: application/json' \
#   -H 'Content-Type: multipart/form-data' \
#   -F 'file=@miku.png'

# http://localhost:8000/knowledge_base/knowledge_base/Hello%20World%204
