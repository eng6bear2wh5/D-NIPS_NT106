
# Real-time Packet Sniffing and Anomaly Detection System Integrated with Distributed Network Intrusion Detection (D-NIDS)

This is a real-time packet monitoring system integrated with a distributed network intrusion detection system (D-NIDS). It captures live network traffic at distributed clients, detects anomalies using machine learning, and confirms threats through a centralized Suricata-based rule engine.

## Project Overview

This system offers decentralized and scalable intrusion detection using:

- Real-time edge anomaly detection at client nodes
- Suricata rule-based verification at a centralized server
- PySide6 dashboard for live alert visualization
- Encrypted communication and database persistence

---

## System Architecture

```
D-NIDS/
├── Client/               # Packet sniffing, feature extraction, ML detection
├── Dashboard/            # GUI visualization using PySide6 + Flask API
├── Server/               # Suricata-based IDS + PostgreSQL storage
├── net_pro/              # Optional network utilities
├── generated-files/      # CSS and UI assets
├── run_client.sh         # Launch client node
├── run_server.sh         # Launch Suricata server
├── run_das.sh            # Launch dashboard
├── run_all.sh            # Orchestrator for full system
└── requirements.txt      # Python dependencies
```

### Client Features
- Captures traffic via `pcap`/`dpkt`
- Extracts features: packet length, time delta, IPs, ports, flows
- Uses `IsolationForest` (scikit-learn) for anomaly detection
- Sends JSON alerts over TCP (encrypted with AES)
- Rich CLI logs and optional PySide6 GUI

### Dashboard Features
- GUI built with PySide6 and Qt Designer
- Communicates with clients via Flask API
- Displays packet summaries, anomaly scores, and alert history

### Server Features
- Receives encrypted anomaly reports from clients
- Converts JSON to PCAP for deep inspection
- Suricata rule-based detection on suspicious flows
- Generates HTML reports with alert severity
- Stores logs in PostgreSQL
- Sends email notifications for high-severity alerts

---

## Security

- Diffie-Hellman key exchange for secure session setup
- AES-256-CBC symmetric encryption with IV randomization
- TCP socket framing with message length prefix

---

## Example Scenarios

### Scenario 1 – Multi-network Monitoring
Clients deployed in different network zones connect to the server and stream encrypted anomaly events.

### Scenario 2 – DDoS ICMP Detection
Server identifies ping flood attacks via Suricata and triggers real-time email alerts.

---

## Deployment Instructions

### Prerequisites
- Python 3.7
- PostgreSQL 13+
- Suricata IDS
- Linux OS Dual Boot Version
- PySide6 - Latest Version

### Installation
```bash
pip install -r requirements.txt
```

### Running the System
```bash
./run_all.sh        # Start all components
./run_server.sh     # Start server
./run_client.sh --interface eth0     # Start client
./run_das.sh        # Start dashboard
```

---

## Repository

GitHub: https://github.com/ursuswh-metamorphic/D-NIPS_NT106

## Demo

o view the project's operation process, you can watch the demo video here:

[![Google Drive](https://img.shields.io/badge/Google%20Drive-Video%20Demo-yellow?style=for-the-badge&logo=googledrive&logoColor=white)](https://drive.google.com/drive/folders/1vw7LXJQ3Ick8RxU8MWXLfjgqUCHScUJQ?usp=drive_link)


