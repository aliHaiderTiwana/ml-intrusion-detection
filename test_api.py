import requests

# The URL where your FastAPI brain is listening
URL = "http://127.0.0.1:8000/predict"

# 🟢 FAKE PACKET 1: Normal Traffic
# A tiny, fast connection (like loading a simple text webpage)
normal_packet = {
    "features": {
        "dur": 0.001,      # 1 millisecond duration
        "sbytes": 100,     # Sent 100 bytes
        "dbytes": 100,     # Received 100 bytes
        "sttl": 31         # Normal Time-To-Live
    }
}

# 🔴 FAKE PACKET 2: Hacker Traffic
# A massive, one-sided data dump (Classic DoS behavior)
hacker_packet = {
    "features": {
        "dur": 10.5,       # Connection held open for 10 seconds!
        "sbytes": 850000,  # Blasting 850,000 bytes at the server
        "dbytes": 0,       # Receiving nothing back
        "sttl": 254        # Max Time-To-Live (often spoofed)
    }
}

print("==================================")
print("🛡️ INITIATING LIVE API TEST 🛡️")
print("==================================\n")

try:
    # Fire the first packet
    print("▶️ Firing Normal Packet...")
    response_1 = requests.post(URL, json=normal_packet)
    print(f"🤖 AI Response: {response_1.json()}\n")

    # Fire the second packet
    print("▶️ Firing Hacker Packet...")
    response_2 = requests.post(URL, json=hacker_packet)
    print(f"🤖 AI Response: {response_2.json()}\n")

except requests.exceptions.ConnectionError:
    print("❌ ERROR: Could not connect to the API. Is your Uvicorn server running?")