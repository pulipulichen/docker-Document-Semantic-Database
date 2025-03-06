#!/bin/bash

curl -X POST http://localhost:8080/process -F "file=@table_1.pdf"
# curl -X POST http://localhost:8080/process -F "file=@table.pdf"
