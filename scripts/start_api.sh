#!/bin/bash
# Start Carbon-Aware Checkout API server

export PYTHONPATH="${PYTHONPATH}:$(pwd)/src"

uvicorn cac.api.checkout_api:app --host 0.0.0.0 --port 8000 --reload
