#!/bin/bash

curl -X POST http://localhost:8080/process -F "file=@Year02.xls"
# curl -X POST http://localhost:8080/process -F "file=@table.pdf"
