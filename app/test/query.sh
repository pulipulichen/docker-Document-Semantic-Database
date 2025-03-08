#!/bin/bash

# curl -X 'POST' \
#   'http://localhost:8000/index/' \
#   -H 'accept: application/json' \
#   -H 'Content-Type: multipart/form-data' \
#   -F 'file=@02.webp' \
#   -F 'document=Hello World'

# curl -X 'POST' \
#   'http://localhost:8000/query' \
#   -H 'accept: application/json' \
#   -H 'Content-Type: multipart/form-data' \
#   -F 'document=行政院'

# curl -X 'POST' \
#   'http://localhost:8000/index/' \
#   -H 'accept: application/json' \
#   -H 'Content-Type: multipart/form-data' \
#   -F 'file=@02.webp'


curl -X 'POST' \
  'http://localhost:8000/query' \
  -H 'accept: application/json' \
  -H 'Content-Type: multipart/form-data' \
  -F 'document=地圖' \
  -F 'query_config={"item_distinct":false}'
