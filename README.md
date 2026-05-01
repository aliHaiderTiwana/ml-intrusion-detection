# Autonomous AI Intrusion Prevention System (IPS) 🛡️

## Overview
This project is a real-time, Artificial Intelligence-driven Intrusion Prevention System (IPS). It actively monitors local network traffic, uses a Machine Learning model to classify packets as "Normal" or "Attack," and automatically updates the Linux firewall to block malicious IP addresses in milliseconds. It includes a live Security Operations Center (SOC) dashboard for real-time monitoring.

**Lead Architect:** Ali Haider Abdullah

## Key Features
* **Real-Time Packet Sniffing:** Bypasses standard OS rules to read raw network packets directly from the network interface card using `scapy`.
* **AI-Powered Analysis:** Utilizes a trained Random Forest model to analyze packet features (size, time-to-live) and classify threats instantly.
* **Autonomous Defense:** Automatically executes root-level `iptables` commands to drop connections from identified threat IPs.
* **Live SOC Dashboard:** A dark-mode, real-time web interface built with React and Tailwind CSS that receives live updates via WebSockets.
* **Local Logging:** All traffic and threat events are securely logged into a local SQLite database for future analysis.

## Technology Stack
* **Backend:** Python, FastAPI, WebSockets, SQLite
* **Machine Learning:** scikit-learn, Pandas, Joblib (Random Forest Classifier)
* **Network Manipulation:** Scapy, Linux `iptables`
* **Frontend:** React, Vite, Tailwind CSS

## How It Works
1. **The Senses:** `sniffer.py` listens to the network interface and extracts key features from incoming IP packets.
2. **The Brain:** The packet data is sent to the FastAPI server, where the AI model evaluates it against trained threat patterns.
3. **The Muscle:** If an attack is detected, the API signals the sniffer to block the source IP using the Ubuntu firewall.
4. **The Interface:** The API simultaneously broadcasts the event over a WebSocket to the React dashboard, updating the UI in real-time.

## Installation & Setup

### Prerequisites
* Linux OS (Ubuntu recommended due to `iptables` dependency)
* Python 3.8+
* Node.js v22+

### 1. Start the AI Backend
Open your first terminal and run:
```bash
# Activate your virtual environment
source venv/bin/activate

# Install requirements (ensure FastAPI, Uvicorn, Scikit-Learn, Pandas are installed)
# Start the API server
uvicorn api:app --reload
