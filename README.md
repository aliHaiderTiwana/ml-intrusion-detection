# 🛡️ AI-Powered Autonomous Cyber Defense System

**Author:** Ali Haider || Abdullah 
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
3. ML Paradigm & JustificationPrimary Paradigm: Supervised Learning (with future expansion into Deep Learning).Justification: Network intrusion detection requires high precision to avoid "false positives" (blocking legitimate users). Since we are using a fully labeled dataset with distinct attack categories, supervised algorithms like Random Forest and XGBoost are ideal. They excel at handling tabular network data, automatically manage non-linear boundaries created by complex attacks, and provide clear feature_importance metrics, which are crucial for explaining the model's decisions during auditing.📊 4. Dataset InformationSource: UNSW-NB15 Dataset (Available on Kaggle)Description:Unlike outdated datasets (e.g., KDD99), UNSW-NB15 reflects modern network traffic and contemporary attack vectors.Size: ~2.5 million total records (Split into 175,341 training and 82,332 testing sets).Features: 49 features representing packet headers and flow-based behaviors (e.g., duration, protocol, bytes sent).Classes: 1 Normal class + 9 Attack families (Fuzzers, Analysis, Backdoors, DoS, Exploits, Generic, Reconnaissance, Shellcode, and Worms).Preprocessing Needs: Categorical feature encoding (One-Hot), numerical scaling (StandardScaler), and class balancing (SMOTE).💻 5. Tools & Technologies StackProgramming Language: Python 3.xMachine Learning: scikit-learn, xgboost, pandas, numpyNetwork & Security: scapy (live packet sniffing), wireshark (analysis)Environment & Deployment: Ubuntu Linux, iptables / ufw (firewall automation), Docker🚧 6. Expected Technical Challenges & MitigationsChallengeDescriptionProposed MitigationClass ImbalanceMalicious traffic is significantly rarer than normal traffic in the dataset, which can cause the model to blindly predict "Normal".Utilize SMOTE (Synthetic Minority Over-sampling Technique) to balance the training data, and evaluate using the F1-Score rather than pure Accuracy.Real-Time LatencyThe model must predict attacks in milliseconds; complex ensembles might introduce lag.Perform strict Feature Selection to train the model only on the top 10-15 most impactful features, reducing computational overhead.Evasion AttacksAttackers may manipulate packet sizes or add noise to trick the classifier.Implement robust preprocessing and test the system against adversarial examples to ensure resilience.
