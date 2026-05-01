from scapy.all import sniff, IP
import requests
import subprocess

API_URL = "http://127.0.0.1:8000/predict"

# CRITICAL: Do not block localhost, or the API and Sniffer will disconnect!
WHITELIST_IPS = {"127.0.0.1", "0.0.0.0"}

# Keep a set of IPs we've already blocked so we don't spam the firewall with duplicate rules
blocked_ips = set()

print("=========================================")
print("🛡️ AUTONOMOUS IPS (DEFENSE) INITIALIZED 🛡️")
print("=========================================")
print("Listening for traffic AND engaging firewall...\n")

def block_ip(ip_address):
    """Executes the Ubuntu iptables command to drop all traffic from the IP"""
    if ip_address not in blocked_ips and ip_address not in WHITELIST_IPS:
        print(f"🧱 [FIREWALL ENGAGED] Blocking IP: {ip_address}")
        try:
            # This is the actual Linux command to block an IP
            subprocess.run(["iptables", "-A", "INPUT", "-s", ip_address, "-j", "DROP"], check=True)
            blocked_ips.add(ip_address)
        except subprocess.CalledProcessError as e:
            print(f"❌ Failed to block {ip_address}. Are you running as root?")

def process_packet(packet):
    if IP in packet:
        source_ip = packet[IP].src
        
        # Skip checking if the IP is already blocked or whitelisted
        if source_ip in blocked_ips or source_ip in WHITELIST_IPS:
            return

        try:
            packet_size = len(packet)
            time_to_live = packet[IP].ttl
            
            live_features = {
                "features": {
                    "sbytes": packet_size,
                    "sttl": time_to_live,
                    "dur": 0.001 
                }
            }

            # Ask the AI
            response = requests.post(API_URL, json=live_features, timeout=1)
            prediction = response.json().get("prediction")
            
            if prediction == "Attack":
                print(f"🚨 [THREAT DETECTED] From: {source_ip} | Size: {packet_size} bytes")
                # Trigger the firewall defense!
                block_ip(source_ip)
                
        except Exception:
            pass

# Start the sniffer
sniff(prn=process_packet, store=False)