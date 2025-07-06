#!/bin/bash

# Chạy Client (nền)
cd Client
source venv/bin/activate
sudo env "PATH=$PATH" "PYTHONPATH=$PYTHONPATH" python3 main.py
cd ..

# Chạy Dashboard API (nền)
Dashboard/.venv/bin/python /home/rigil/PacketSniffer/D-NIPS_NT106/Dashboard/main.py &
DASH_PID=$!

# Đợi các tiến trình con
kill $DASH_PID