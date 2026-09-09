# 🚀 ReconRadar QUANTUM v8.0

<div align="center">

![ReconRadar Banner](screenshots/banner.svg)

**Enterprise-Grade Security Intelligence & Reconnaissance Platform**

[![Python](https://img.shields.io/badge/Python-3.8%2B-f97316?style=flat-square&logo=python&logoColor=white)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.100%2B-0ea5e9?style=flat-square&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com)
[![WebSocket](https://img.shields.io/badge/WebSocket-Realtime-f43f5e?style=flat-square)](https://developer.mozilla.org/en-US/docs/Web/API/WebSockets_API)
[![License](https://img.shields.io/badge/License-MIT-10b981?style=flat-square)](LICENSE)
[![Version](https://img.shields.io/badge/Version-8.0.0-f97316?style=flat-square)]()

> ⚠️ **For authorized security testing only.** Always obtain proper written authorization before scanning any target.

</div>

---

## 📖 Table of Contents

- [Overview](#-overview)
- [Features](#-features)
- [Quick Start](#-quick-start)
- [Installation](#-installation)
- [Usage Guide](#-usage-guide)
- [Architecture](#-architecture)
- [Configuration](#-configuration)
- [API Reference](#-api-reference)
- [Troubleshooting](#-troubleshooting)
- [Security Notice](#-security-notice)
- [Contributing](#-contributing)
- [License](#-license)

---

## 🎯 Overview

**ReconRadar QUANTUM** is a professional-grade security intelligence platform designed for penetration testers, security researchers, and red teams. It combines passive OSINT gathering with active reconnaissance capabilities in a modern, enterprise-ready interface.

### Key Capabilities

- 🔍 **Multi-Vector Reconnaissance** — DNS, WHOIS, subdomain enumeration, port scanning
- 🌐 **OSINT Intelligence** — 115+ data sources including Shodan, Censys, VirusTotal
- 📸 **Automated Screenshots** — Visual reconnaissance via Playwright
- ☁️ **Cloud Asset Discovery** — AWS S3, Azure Blob, GCP Storage enumeration
- 🔐 **Hash Cracker** — MD5, SHA1, SHA256, SHA512, NTLM support
- 📊 **Real-time Reporting** — Live WebSocket updates with professional findings cards
- 💾 **Persistent Storage** — SQLAlchemy ORM with SQLite/PostgreSQL support

---

## ✨ Features

### Passive Reconnaissance

| Module | Description |
|--------|-------------|
| **DNS Enumeration** | A, MX, TXT, NS, SOA, CNAME, AAAA records via `dnspython` |
| **WHOIS Lookup** | Intelligent 24-hour caching via SQLAlchemy |
| **Certificate Transparency** | Passive subdomain discovery via `crt.sh` + permutation scanning |
| **Zone Transfer** | AXFR query against discovered nameservers |
| **OSINT Sources** | Shodan, Censys, VirusTotal, AlienVault, Hunter.io, HaveIBeenPwned |

### Active Reconnaissance

| Module | Description |
|--------|-------------|
| **Subdomain Enumeration** | CT logs + brute-force + permutation scanning |
| **Technology Fingerprinting** | Wappalyzer-style detection with CVE correlation |
| **Port Scanning** | `python-nmap` with configurable arguments |
| **Vulnerability Detection** | Security headers, path brute-force, version disclosure |
| **API Discovery** | GraphQL, Swagger, REST endpoint mapping |
| **Cloud Enumeration** | AWS S3, Azure Blob, GCP bucket discovery |

### Hash Cracker Module

| Algorithm | Support | Attack Methods |
|-----------|---------|----------------|
| **MD5** | ✅ | Dictionary, Rule-Based, Brute-Force |
| **SHA1** | ✅ | Dictionary, Rule-Based, Brute-Force |
| **SHA256** | ✅ | Dictionary, Rule-Based, Brute-Force |
| **SHA384** | ✅ | Dictionary, Rule-Based, Brute-Force |
| **SHA512** | ✅ | Dictionary, Rule-Based, Brute-Force |
| **NTLM** | ✅ | Dictionary, Rule-Based, Brute-Force |
| **Base64** | ✅ | Auto-decode |

---

## ⚡ Quick Start

```bash
# Clone repository
git clone https://github.com/Nexvir/reconradar.git
cd reconradar

# Install dependencies
pip install -r requirements.txt

# Launch application
python3 backend.py

# Access web interface
# Open http://localhost:8000 in your browser
```

---

## 📦 Installation

### Prerequisites

- **Python 3.8+** (tested on 3.12)
- **Nmap** (`apt install nmap` or `brew install nmap`)
- **Optional:** Playwright for screenshots (`playwright install`)

### Dependencies

```bash
# Core requirements
pip install fastapi>=0.100.0
pip install uvicorn>=0.23.0
pip install python-nmap>=0.7.1
pip install dnspython>=2.4.0
pip install python-whois>=0.8.0
pip install httpx>=0.25.0

# Optional: Database (PostgreSQL)
pip install psycopg2-binary sqlalchemy

# Optional: Screenshots
pip install playwright
playwright install chromium
```

### Docker (Coming Soon)

```bash
docker pull nexvir/reconradar:quantum
docker run -p 8000:8000 nexvir/reconradar:quantum
```

---

## 📘 Usage Guide

### Basic Scan

1. **Enter Target**: Input domain or IP in the target field (e.g., `example.com`)
2. **Select Profile**: Choose scan intensity (Quick, Standard, Comprehensive, Stealth)
3. **Configure Modules**: Enable/disable reconnaissance modules
4. **Start Scan**: Click the scan button or press Enter

### Scan Profiles

| Profile | Speed | Stealth | Modules |
|---------|-------|---------|---------|
| **Quick** | Fast | High | DNS, WHOIS only |
| **Standard** | Medium | Medium | DNS, WHOIS, Subdomains, Ports |
| **Comprehensive** | Slow | Low | All modules enabled |
| **Stealth** | Very Slow | Very High | Rate-limited passive only |

### Advanced Options

```bash
# Custom Nmap arguments
--rate-limit 100 --timeout 30 -sV

# API Key for external services
Add your API key for Shodan, VirusTotal, etc.
```

### Hash Cracker

1. Enable "Hash Cracker" module in sidebar
2. Enter hash value in the hash input field
3. Select hash type (or auto-detect)
4. Click "Crack Hash"

---

## 🏗 Architecture

```
┌─────────────────────────────────────────────────────────┐
│                   ReconRadar QUANTUM                     │
├─────────────────────────────────────────────────────────┤
│                                                          │
│  ┌──────────────┐    ┌──────────────┐    ┌───────────┐ │
│  │   Frontend   │◄──►│   Backend    │◄──►│ WebSocket │ │
│  │  (Glassmorphism)│  │  (FastAPI)   │  │   Layer   │ │
│  └──────────────┘    └──────────────┘    └───────────┘ │
│         │                   │                           │
│         ▼                   ▼                           │
│  ┌──────────────┐    ┌──────────────┐                  │
│  │  UI Components│   │  Scan Engine │                  │
│  │  - Sidebar   │    │  - DNS       │                  │
│  │  - Terminal  │    │  - WHOIS     │                  │
│  │  - Results   │    │  - Nmap      │                  │
│  └──────────────┘    │  - OSINT     │                  │
│                      │  - Hash      │                  │
│                      └──────────────┘                  │
│                             │                           │
│                             ▼                           │
│                      ┌──────────────┐                  │
│                      │   Database   │                  │
│                      │  (SQLAlchemy)│                  │
│                      └──────────────┘                  │
│                                                          │
└─────────────────────────────────────────────────────────┘
```

### Component Breakdown

| File | Purpose | Lines |
|------|---------|-------|
| `backend.py` | FastAPI server, WebSocket handler, scan orchestration | ~1,824 |
| `frontend.py` | HTML template, CSS design system, JavaScript client | ~1,834 |
| `database.py` | SQLAlchemy models, ORM layer, caching | ~473 |
| `hash_cracker.py` | Hash cracking engine, wordlist management | ~558 |
| `hacker_enhanced.py` | Advanced recon modules, cloud discovery | ~550 |

---

## ⚙ Configuration

### Environment Variables

```bash
# Database
DATABASE_URL=sqlite:///reconradar.db
# DATABASE_URL=postgresql://user:pass@localhost/reconradar

# API Keys (optional)
SHODAN_API_KEY=your_shodan_key
VIRUSTOTAL_API_KEY=your_vt_key
CENSYS_API_ID=your_censys_id
CENSYS_API_SECRET=your_censys_secret

# Server
HOST=0.0.0.0
PORT=8000
DEBUG=false
```

### Custom Wordlists

Place custom wordlists in the `data/` directory:

```
data/
├── wordlist.json      # Default subdomain list
├── paths.txt          # Directory brute-force list
├── signatures.json    # Technology detection patterns
└── osint.txt          # OSINT source configuration
```

---

## 🔌 API Reference

### WebSocket Endpoint

**URL:** `ws://localhost:8000/ws`

#### Client → Server Messages

```json
{
  "type": "start_scan",
  "target": "example.com",
  "profile": "standard",
  "modules": ["dns", "whois", "subdomains", "ports"],
  "args": "--rate-limit 100",
  "api_key": "optional_key"
}
```

```json
{
  "type": "crack_hash",
  "hash": "5d41402abc4b2a76b9719d911017c592",
  "hash_type": "md5"
}
```

```json
{
  "type": "stop_scan"
}
```

#### Server → Client Messages

```json
{
  "type": "status",
  "scanning": true,
  "target": "example.com",
  "modules": ["dns", "whois"],
  "progress": 45
}
```

```json
{
  "type": "log",
  "level": "info",
  "message": "Found subdomain: mail.example.com"
}
```

```json
{
  "type": "result",
  "category": "subdomain",
  "title": "mail.example.com",
  "description": "Resolves to 192.168.1.100",
  "severity": "low",
  "meta": "A record: 192.168.1.100"
}
```

### REST Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/` | Web interface |
| `GET` | `/api/scans` | List all scans |
| `GET` | `/api/scans/{id}` | Get scan details |
| `POST` | `/api/scans` | Start new scan |
| `DELETE` | `/api/scans/{id}` | Stop/delete scan |
| `GET` | `/api/findings` | List all findings |
| `GET` | `/api/export/{id}` | Export scan report |

---

## 🔧 Troubleshooting

### Common Issues

#### 1. WebSocket Connection Failed

**Symptom:** Status shows "Disconnected"

**Solution:**
- Check if server is running on correct port
- Verify no firewall blocking WebSocket connections
- Try refreshing the page

#### 2. Nmap Not Found

**Symptom:** Port scanning fails with "nmap not found"

**Solution:**
```bash
# Ubuntu/Debian
sudo apt install nmap

# macOS
brew install nmap

# Windows
Download from https://nmap.org/download.html
```

#### 3. Database Lock Error

**Symptom:** "database is locked" error

**Solution:**
- Stop the application
- Delete `reconradar.db` (backup first if needed)
- Restart application

#### 4. Module Import Errors

**Symptom:** "ModuleNotFoundError"

**Solution:**
```bash
pip install -r requirements.txt --upgrade
```

### Performance Optimization

- **Reduce concurrent modules** for slower networks
- **Use Stealth profile** for large targets
- **Enable caching** to avoid redundant lookups
- **Increase rate limits** cautiously on fast connections

---

## 🔒 Security Notice

### Authorized Use Only

This tool is designed for **legitimate security testing** purposes only. Users must:

1. ✅ Obtain **written authorization** from target owners
2. ✅ Comply with all applicable laws and regulations
3. ✅ Follow responsible disclosure practices
4. ✅ Never scan systems without explicit permission

### Legal Disclaimer

The developers assume **no liability** for misuse of this software. Users are solely responsible for compliance with applicable laws including:

- Computer Fraud and Abuse Act (CFAA) - USA
- Computer Misuse Act - UK  
- Cybercrime laws in your jurisdiction
- Data protection regulations (GDPR, etc.)

---

## 🤝 Contributing

We welcome contributions! Please follow these guidelines:

### Development Setup

```bash
# Fork and clone
git clone https://github.com/YOUR_USERNAME/reconradar.git
cd reconradar

# Create branch
git checkout -b feature/your-feature-name

# Make changes and test
# Commit with clear messages
git commit -m "feat: add new recon module"

# Push and create PR
git push origin feature/your-feature-name
```

### Code Standards

- **Python:** PEP 8 compliant
- **JavaScript:** ES6+, strict mode
- **CSS:** BEM naming convention
- **Commits:** Conventional Commits specification

### Pull Request Template

```markdown
## Description
Brief description of changes

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Breaking change
- [ ] Documentation update

## Testing
- [ ] Tested locally
- [ ] Added unit tests
- [ ] Updated documentation

## Checklist
- [ ] Code follows style guidelines
- [ ] Self-review completed
- [ ] No new warnings introduced
```

---

## 📄 License

**MIT License**

Copyright (c) 2024 ReconRadar

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

---

## 📞 Support

- **Documentation:** [View Docs](#)
- **Issues:** [GitHub Issues](https://github.com/Nexvir/reconradar/issues)
- **Discussions:** [GitHub Discussions](https://github.com/Nexvir/reconradar/discussions)
- **Email:** security@reconradar.io (for vulnerabilities only)

---

<div align="center">

**Built with ❤️ by the ReconRadar Team**

[![GitHub](https://img.shields.io/badge/GitHub-Nexvir-white?style=flat-square&logo=github)](https://github.com/Nexvir)
[![Twitter](https://img.shields.io/badge/Twitter-@reconradar-1DA1F2?style=flat-square&logo=twitter)]()

⭐ Star this repo if you find it useful!

</div>
