# 🛡️ AI-Powered Autonomous Cyber Defense System

**Author:** Ali Haider  
**Course:** CSC-361 Machine Learning | Spring 2025  
**Track:** Track B - Software-Based AI System  
**Instructor:** Dr. Shafiq Ur Rehman Khan  

---

## 📌 1. Problem Definition & Target Audience
Traditional rule-based security firewalls are slow, reactive, and incapable of detecting "Zero-Day" attacks or complex behavioral anomalies. This project builds an **Intrusion Detection and Prevention System (IDPS)** that utilizes Machine Learning to analyze network traffic in real-time, instantly distinguishing between legitimate user activity and malicious attacks.

**Target Audience:**
* **Small to Medium Enterprises (SMEs):** Organizations lacking the budget for a 24/7 manual Security Operations Center (SOC).
* **Cloud Service Providers:** To provide an automated layer of defense for hosted virtual machines.
* **IoT Network Administrators:** Securing networks of vulnerable smart devices against botnets.

---

## 🏗️ 2. System Architecture
The system follows a continuous pipeline from data capture to autonomous response.

```mermaid
graph TD
    A[Live Network Interface / UNSW-NB15] -->|Raw Packets| B(Data Preprocessing Layer)
    B -->|Encoding & Scaling| C{Feature Engineering}
    C -->|Top Features| D[Supervised ML Engine]
    
    subgraph Detection Engine
    D -->|Classification| E{Traffic Analysis}
    end
    
    E -- Attack Detected --> F[Generate Alert]
    E -- Normal Traffic --> G[Allow Connection]
    
    subgraph Autonomous Response
    F --> H[Trigger Python Response Script]
    H --> I((Block IP via Linux iptables))
    end
