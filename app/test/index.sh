#!/bin/bash

# curl -X 'POST' \
#   'http://localhost:8000/index/' \
#   -H 'accept: application/json' \
#   -H 'Content-Type: multipart/form-data' \
#   -F 'file=@02.webp' \
#   -F 'document=Hello World'

# curl -X 'POST' \
#   'http://localhost:8000/index/' \
#   -H 'accept: application/json' \
#   -H 'Content-Type: multipart/form-data' \
#   -F 'document=Hello World 4' \
#   -F 'metadata={"a":1,"b":2,"c":3}'

# curl -X 'POST' \
#   'http://localhost:8000/index/' \
#   -H 'accept: application/json' \
#   -H 'Content-Type: multipart/form-data' \
#   -F 'file=@02.webp'

curl -X 'POST' \
  'http://localhost:8000/index/' \
  -H 'accept: application/json' \
  -H 'Content-Type: multipart/form-data' \
  -F 'file=@example.pdf'
