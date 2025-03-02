#!/bin/bash

# Cài đặt Chromium trên Linux
apt-get update && apt-get install -y chromium-browser
pip install -r requirements.txt
python -m uvicorn main:app --host 0.0.0.0 --port 10000