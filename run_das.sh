#!/bin/bash

# Chạy Dashboard GUI (nền)
cd Dashboard
source .venv/bin/activate
python3 main.py &
DASH_PID=$!
cd ..