#!/bin/bash

# uvicorn main:app --host 0.0.0.0 --port 8000 --workers ${UVICORN_WORKERS}
uvicorn main:app --host 0.0.0.0 --port 8000 --reload