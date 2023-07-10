#!/bin/sh

port=${PORT-8000}
workers=${WORKERS-4}

cd webtronics && alembic upgrade head && python initial_data.py
cd ../ && uvicorn webtronics.application:app --host 0.0.0.0 --workers "$workers" --port "$port"