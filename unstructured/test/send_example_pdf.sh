#!/bin/bash

curl -X POST http://localhost:8080/process -F "file=@example.pdf"
