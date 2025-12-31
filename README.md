# Adaptive Honeypot Mini-Lab

A small-scale honeypot system that **dynamically reconfigures itself based on attacker behavior**.  
It emulates fake services (SSH, HTTP, FTP), analyzes attack patterns, and integrates with SIEM systems to tag logs.  
Designed as a **short-term demo project**, deployable on Raspberry Pi or Docker.

---

## Features

- Adaptive engine that changes honeypot services in real time.
- Fake SSH, HTTP, and FTP services for attacker interaction.
- Attack pattern analysis with rule-based or ML-based detection.
- SIEM integration (Splunk, ELK, Graylog).
- Optional dashboard for visualization.
- Lightweight deployment on Raspberry Pi or Docker.

---

## Project Structure

```
adaptive-honeypot/
│
├── README.md
├── LICENSE                
├── requirements.txt       
├── docker-compose.yml     
│
├── config/
│   ├── settings.yaml        # General settings (ports, services, SIEM integration)
│   └── rules.yaml           # Behavior rules (e.g., brute force → service switch)
│
├── core/
│   ├── __init__.py
│   ├── honeypot.py          # Honeypot core logic
│   ├── ssh_service.py       # Fake SSH service
│   ├── http_service.py      # Fake HTTP service
│   └── ftp_service.py       # Optional fake FTP service
│
├── analysis/
│   ├── __init__.py
│   ├── log_collector.py     # Collects logs
│   ├── pattern_analyzer.py  # Regex/ML-based attack analysis
│   └── decision_engine.py   # Adaptive service switching
│
├── integration/
│   ├── __init__.py
│   ├── siem_connector.py    # Splunk/ELK integration
│   ├── alert_system.py      # Email/webhook alerts
│   └── dashboard.py         # Flask/Django visualization
│
├── deployment/
│   ├── dockerfile           # Docker image
│   ├── vagrantfile          # Optional VM setup
│   └── sandbox_setup.sh     # Isolation script
│
└── tests/
    ├── test_core.py         # Tests for honeypot modules
    ├── test_analysis.py     # Tests for analyzer & decision engine
    └── test_integration.py  # Tests for SIEM & alert system
```

---

## Quick Start

### 1. Clone the repository
```bash
git clone https://github.com/yourusername/adaptive-honeypot-mini-lab.git
cd adaptive-honeypot-mini-lab
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Run the honeypot
```bash
python core/honeypot.py
```

### 4. (Optional) Run with Docker
```bash
docker-compose up --build
```

---

## Example Workflow

1. Attacker connects to fake SSH service.  
2. Log collector records the attempt.  
3. Pattern analyzer detects brute force.  
4. Decision engine switches honeypot to HTTP mode.  
5. SIEM connector tags the event as `SSH → HTTP attack chain`.  
6. Dashboard displays the incident in real time.  

---

## Disclaimer

This project is for **educational and research purposes only**.  
Do not deploy in production environments or expose to the public internet.  
Use in controlled lab settings.

---

## License

Apache-2.0 License – free to use, modify, and share with attribution.
