#!/bin/bash
# Cài đặt Google Chrome trên Ubuntu
apt-get update && apt-get install -y wget unzip
wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
apt-get install -y ./google-chrome-stable_current_amd64.deb
pip install -r requirements.txt
python -m uvicorn main:app --host 0.0.0.0 --port 10000