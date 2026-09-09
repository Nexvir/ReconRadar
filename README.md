<div align="center">

![ReconRadar Banner](screenshots/banner.svg)

# ReconRadar APOLLO v7.0 HACKER EDITION

**Advanced OSINT, Reconnaissance & Penetration Testing Platform with Hash Cracking**

[![Python](https://img.shields.io/badge/Python-3.8%2B-00ff9d?style=flat-square&logo=python&logoColor=white)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.100%2B-00d4ff?style=flat-square&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com)
[![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-2.0-e74c3c?style=flat-square&logo=database&logoColor=white)](https://sqlalchemy.org)
[![License](https://img.shields.io/badge/License-MIT-a855f7?style=flat-square)](LICENSE)
[![WebSocket](https://img.shields.io/badge/WebSocket-Live_Stream-ef4444?style=flat-square)](https://developer.mozilla.org/en-US/docs/Web/API/WebSockets_API)
[![Nmap](https://img.shields.io/badge/Nmap-Required-f59e0b?style=flat-square)](https://nmap.org)
[![Hash Cracker](https://img.shields.io/badge/Hash_Cracker-MD5_SHA_NTLM-9b59b6?style=flat-square)]()
[![GitHub](https://img.shields.io/badge/GitHub-Nexvir-white?style=flat-square&logo=github)](https://github.com/Nexvir)

> ⚠️ **For authorized security testing and ethical hacking only.** Always obtain proper written permission before scanning any target.

</div>

---

## 📸 Screenshots

### Dashboard — Live Reconnaissance & Hacker Tools

![Dashboard](screenshots/dashboard.svg)

*Real-time WebSocket dashboard with advanced recon modules, hash cracker, and cyberpunk-themed UI.*

---

### Intelligence Report Output

![Report](screenshots/report.svg)

*Auto-generated HTML intelligence report with attack chain analysis, cloud assets, and vulnerability correlations.*

---

### Hash Cracker Interface

![Hash Cracker](screenshots/hash_cracker.svg)

*Professional hash cracking interface supporting multiple algorithms and attack methods.*

---

### Architecture Overview

![Architecture](screenshots/architecture.svg)

*ReconRadar v7.0 architecture: FastAPI backend, database layer, 7+ hacker modules, and persistent storage.*

---

## 🌟 Features

### 🔍 Advanced Passive Reconnaissance
- **DNS enumeration** — A, MX, TXT, NS, SOA, CNAME, AAAA records via `dnspython`
- **WHOIS lookup** — with intelligent 24-hour caching via SQLAlchemy
- **Certificate transparency** — passive subdomain discovery via `crt.sh` + permutation scanning
- **Zone transfer attempts** — AXFR query against discovered nameservers
- **115+ OSINT sources** — Shodan, Censys, VirusTotal, AlienVault, Hunter.io, HaveIBeenPwned, Google Dorks

### ⚡ Active Reconnaissance & Hacker Modules
- **Advanced Subdomain Enumeration** — CT logs + brute-force + permutation scanning
- **Technology Fingerprinting** — Wappalyzer-style detection with CVE correlation
- **Screenshot Capture** — Automated browser screenshots via Playwright
- **API Endpoint Discovery** — GraphQL, Swagger, REST API mapping
- **Cloud Asset Discovery** — AWS S3, Azure Blob, GCP Storage bucket enumeration
- **Credential Leak Detection** — GitHub dorking + breach database integration
- **Port scanning** — `python-nmap` with socket fallback; configurable arguments
- **Vulnerability scanning** — Security headers, path brute-force, version disclosure
- **Attack Chain Analysis** — Correlate findings to identify exploitation paths

### 🔐 Hash Cracker Module
- **Supported Algorithms**: MD5, SHA1, SHA256, SHA384, SHA512, NTLM, Base64
- **Attack Methods**:
  - Dictionary Attack (with common passwords + custom wordlists)
  - Rule-Based Attack (mutations, leetspeak, capitalization)
  - Brute-Force Attack (configurable charset and length)
- **Auto-Detection** — Automatically identifies hash type
- **Database Integration** — Stores cracked hashes for future reference
- **History Tracking** — View all previously cracked hashes

### 🗄️ Professional Database Layer
- **SQLAlchemy ORM** — SQLite by default, PostgreSQL ready
- **7 Core Tables**:
  - `scans` — Scan metadata and status
  - `findings` — All discovered assets and vulnerabilities
  - `screenshots` — Captured webpage screenshots
  - `targets` — Target tracking over time
  - `api_keys` — Authentication and rate limiting
  - `cache` — Intelligent DNS/WHOIS/Nmap caching
  - `cracked_hashes` — Hash cracking history and results
- **Persistent Storage** — Never lose scan results
- **Advanced Queries** — Filter, search, and export findings
- **Audit Logging** — Complete track of all operations

### 📊 Reporting & Storage
- **Live WebSocket stream** — Real-time results pushed to browser
- **Auto-generated HTML reports** — Saved to `reports/{scan_id}.html`
- **Scan history** — Database-backed with REST API `GET /history`
- **Hash cracking history** — Track all cracking attempts
- **Rotating logs** — `reconradar.log` up to 10 MB × 5 backups

### 🧠 Smart Caching & Performance
- DNS results cached for **5 minutes** (database-backed)
- WHOIS results cached for **24 hours** (database-backed)
- Nmap results cached per target
- Hash cracking results permanently stored
- Connection pooling for optimal database performance

### 🛡️ Security Enhancements
- **Input Validation** — Prevents SSRF and injection attacks
- **Rate Limiting** — Per-API-key throttling
- **API Key Authentication** — Secure access control
- **Audit Logging** — Complete operation tracking
- **Secure Credential Handling** — No plaintext passwords in logs

---

## 🏗️ Architecture

```
reconradar/
├── backend.py              ← FastAPI app, REST API, WebSocket hub
├── frontend.py             ← Cyberpunk-themed HTML/CSS/JS dashboard
├── database.py             ← SQLAlchemy ORM, models, CRUD operations
├── hacker_enhanced.py      ← Advanced hacker modules (subdomain, tech, cloud, etc.)
├── hash_cracker.py         ← Hash cracking engine with multiple methods
├── data/
│   ├── subdomains.txt      ← Subdomain wordlist (~500 entries)
│   ├── paths.txt           ← Path brute-force wordlist
│   ├── signatures.json     ← Vuln signatures and tech patterns
│   ├── osint.txt           ← OSINT source definitions (115+ entries)
│   └── wordlist.json       ← Password wordlist for hash cracking
├── reports/
│   ├── index.json          ← Scan history index (legacy)
│   └── *.html              ← Per-scan intelligence reports
├── reconradar.db           ← SQLite database (auto-created)
└── reconradar.log          ← Rotating application log
```

### Module Flow

```
Browser ──WebSocket──► FastAPI Backend ──► Database Layer
                            │
        ┌───────────────────┼─────────────────────┐
        ▼                   ▼                     ▼
   Recon Modules      Hacker Modules        Hash Cracker
   - DNS/WHOIS        - Subdomain enum      - MD5/SHA/NTLM
   - Port scan        - Tech fingerprint    - Dictionary/Brute
   - HTTP vulns       - Cloud discovery     - Rule-based
   - OSINT 115+       - API mapping         - Auto-detect
   - Screenshots      - Credential leaks    - Store results
        │                   │                     │
        └───────────────────┴─────────────────────┘
                                    │
                      database.db + reports/ + logs + cache
```

---

## 🚀 Installation

### Prerequisites

- **Python 3.8+**
- **Nmap** installed on the system
- **Optional**: Playwright (for screenshots), PostgreSQL (for production DB)

```bash
# Ubuntu / Debian
sudo apt install nmap python3-pip
pip3 install playwright
playwright install chromium

# macOS (Homebrew)
brew install nmap
pip3 install playwright
playwright install chromium

# Windows
# Download Nmap from https://nmap.org/download.html
# pip install playwright
# playwright install chromium
```

### Step 1 — Clone the repository

```bash
git clone https://github.com/Nexvir/reconradar.git
cd reconradar
```

### Step 2 — Install Python dependencies

```bash
pip install fastapi uvicorn python-nmap dnspython python-whois httpx sqlalchemy aiosqlite passlib
```

Or install everything at once:

```bash
pip install -r requirements.txt
```

> **Note:** `httpx`, `python-nmap`, `dnspython`, `python-whois`, and `playwright` are gracefully optional — the tool falls back to stdlib if they're missing.

### Step 3 — Initialize Database & Run

```bash
python backend.py
```

The database (`reconradar.db`) will be auto-created on first run.

Then open your browser at:

```
http://localhost:8000
```

---

## 💻 Usage

### Basic Reconnaissance Scan

1. Open `http://localhost:8000` in your browser
2. Navigate to **RECON** tab
3. Enter the target domain (e.g. `example.com`)
4. Select modules (DNS, Subdomains, Ports, HTTP, Vulns, OSINT, Screenshots)
5. Click **⚡ SCAN** — results stream live via WebSocket
6. View saved reports in database or `reports/` folder

### Hash Cracking

1. Navigate to **HASH CRACKER** tab
2. Enter hash value (e.g. `5f4dcc3b5aa765d61d8327deb882cf99`)
3. Select algorithm (or use Auto-Detect)
4. Choose attack method:
   - **Dictionary** — Uses built-in + custom wordlists
   - **Rule-Based** — Applies mutations (leet, caps, numbers)
   - **Brute-Force** — Tries all combinations (slow but thorough)
5. Click **🔓 CRACK**
6. View results instantly + saved in database history

### Advanced Nmap Arguments

Pass custom Nmap flags in the UI:

| Flag | Description |
|------|-------------|
| `-sV` | Service/version detection |
| `-sS` | SYN stealth scan *(requires root)* |
| `-O` | OS detection *(requires root)* |
| `-p 1-65535` | Full port range |
| `-T4` | Aggressive timing |
| `--script=default` | NSE default scripts |

### API Usage

#### Crack a Hash

```bash
curl -X POST http://localhost:8000/hash/crack \
  -H "Content-Type: application/json" \
  -d '{
    "hash": "5f4dcc3b5aa765d61d8327deb882cf99",
    "algorithm": "md5",
    "method": "dictionary"
  }'
```

#### Get Crack History

```bash
curl http://localhost:8000/hash/history
```

#### Get System Statistics

```bash
curl http://localhost:8000/stats
```

#### View Scan History

```bash
curl http://localhost:8000/history
```

### Run as Root (full capabilities)

```bash
sudo python backend.py
```

Root access unlocks SYN scan (`-sS`), OS detection (`-O`), and advanced Nmap features.

---

## 🔧 Configuration

### Database Configuration

Edit `database.py` to switch from SQLite to PostgreSQL:

```python
# SQLite (default)
DATABASE_URL = "sqlite:///reconradar.db"

# PostgreSQL (production)
# DATABASE_URL = "postgresql://user:password@localhost:5432/reconradar"
```

### Wordlists & Data Files

All data files are editable:

| File | Purpose | Format |
|------|---------|--------|
| `data/subdomains.txt` | Subdomain brute-force | One prefix per line |
| `data/paths.txt` | HTTP path brute-force | One URL path per line |
| `data/osint.txt` | OSINT sources | `NAME\|TYPE\|URL\|CONFIDENCE` |
| `data/signatures.json` | Tech/vuln signatures | JSON array |
| `data/wordlist.json` | Password wordlist | JSON array |

### Caching Tuning

Edit in `database.py`:

```python
DNS_CACHE_TTL   = 300      # 5 minutes
WHOIS_CACHE_TTL = 86400    # 24 hours
NMAP_CACHE_TTL  = 3600     # 1 hour
```

### Hash Cracker Settings

Edit in `hash_cracker.py`:

```python
MAX_BRUTE_LENGTH = 6       # Max length for brute-force
DICTIONARY_LIMIT = 10000   # Max words per crack attempt
```

---

## 📡 What ReconRadar Discovers

### DNS & WHOIS
- A, AAAA, MX, TXT, NS, SOA, CNAME records
- WHOIS registration data (registrar, dates, nameservers)
- Zone transfer (AXFR) attempts

### Subdomains
- **Passive** — Certificate transparency via `crt.sh`
- **Active** — Brute-force + permutation scanning
- **Takeover verification** — 45+ cloud provider checks

### Port Scanning
Default ports: `21, 22, 25, 80, 443, 3306, 5432, 6379, 8080, 8443, 27017`

### Technology Stack
- Web servers (Apache, Nginx, IIS)
- CMS (WordPress, Drupal, Joomla)
- Frameworks (Django, Flask, Laravel, Express)
- JavaScript libraries (React, Vue, Angular)
- Analytics, Ads, Tag managers

### Vulnerability Checks
| Finding | Severity |
|---------|---------|
| Missing HSTS | 🔴 High |
| Missing CSP | 🟡 Medium |
| Missing X-Frame-Options | 🟡 Medium |
| Server version disclosure | 🔵 Low |
| Exposed admin panels | 🟠 Critical |
| Cloud bucket misconfiguration | 🟠 Critical |

### Cloud Assets
- AWS S3 buckets
- Azure Blob Storage
- Google Cloud Storage
- DigitalOcean Spaces

### API Endpoints
- GraphQL endpoints
- Swagger/OpenAPI docs
- REST API routes
- Admin interfaces

### Hash Cracking
| Algorithm | Speed | Success Rate |
|-----------|-------|--------------|
| MD5 | ⚡⚡⚡ | High |
| SHA1 | ⚡⚡ | Medium |
| SHA256 | ⚡ | Low-Medium |
| NTLM | ⚡⚡⚡ | High |
| Base64 | ⚡⚡⚡⚡ | Very High |

---

## 🔌 API Reference

### REST Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/` | Serves the HTML dashboard |
| `POST` | `/hash/crack` | Crack a hash |
| `GET` | `/hash/history` | Get crack history |
| `GET` | `/history` | Get scan history |
| `GET` | `/history/{scan_id}` | Get specific scan report |
| `GET` | `/stats` | Get system statistics |

### WebSocket

```
ws://localhost:8000/ws
```

**Send a recon scan request:**
```json
{
  "target": "example.com",
  "nmap_args": "-sV -T4",
  "modules": {
    "dns": true,
    "subdomains": true,
    "ports": true,
    "http": true,
    "vulns": true,
    "osint": true,
    "screenshots": true
  }
}
```

**Send a hash crack request:**
```json
{
  "hash": "5f4dcc3b5aa765d61d8327deb882cf99",
  "algorithm": "md5",
  "method": "dictionary"
}
```

**Receive messages:**
```json
{ "type": "log",    "msg": "Starting DNS enumeration..." }
{ "type": "result", "col1": "example.com", "col2": "A Record", "col3": "93.184.216.34", "severity": "Info" }
{ "type": "hash_result", "hash": "...", "plaintext": "password", "method": "dictionary" }
{ "type": "status", "status": "complete" }
```

---

## ⚙️ Dependencies

| Package | Purpose | Required |
|---------|---------|---------|
| `fastapi` | Web framework & REST API | ✅ |
| `uvicorn` | ASGI server | ✅ |
| `sqlalchemy` | Database ORM | ✅ |
| `aiosqlite` | Async SQLite driver | ✅ |
| `python-nmap` | Nmap Python bindings | ⚠️ Optional |
| `dnspython` | Advanced DNS queries | ⚠️ Optional |
| `python-whois` | WHOIS lookups | ⚠️ Optional |
| `httpx` | Async HTTP client | ⚠️ Optional |
| `passlib` | Hash handling | ✅ |
| `playwright` | Screenshot capture | ⚠️ Optional |
| `nmap` (binary) | Port scanning | ✅ System dependency |

---

## 🛡️ Ethical & Legal Notice

> **ReconRadar is a professional security and penetration testing tool. Use it responsibly and ethically.**

- ✅ Use only on systems you **own** or have **explicit written permission** to test
- ✅ Use for bug bounty hunting, penetration testing, and security research
- ✅ Respect rate limits and terms of service of third-party OSINT sources
- ❌ Do **not** use for unauthorized reconnaissance, surveillance, or attacks
- ❌ Do **not** use against production systems without a signed scope agreement
- ❌ Do **not** use hash cracking for unauthorized password recovery

**The author assumes no liability for misuse.** This tool is provided for authorized security professionals, ethical hackers, and researchers only.

---

## 🗺️ Roadmap

- [ ] Machine Learning for vulnerability prediction
- [ ] Integration with Nessus/OpenVAS
- [ ] Dark Web Monitoring
- [ ] Scheduled scans with cron
- [ ] Docker containerization
- [ ] Slack/Discord webhook notifications
- [ ] PDF/Excel report export
- [ ] Multi-user support with roles
- [ ] GraphQL API
- [ ] Mobile responsive UI

---

## 🤝 Contributing

Pull requests are welcome! For major changes, please open an issue first.

```bash
# Fork & clone
git clone https://github.com/Nexvir/reconradar.git
cd reconradar

# Create a feature branch
git checkout -b feature/my-new-module

# Commit & push
git commit -m "feat: add advanced hash cracker"
git push origin feature/my-new-module

# Open a Pull Request on GitHub
```

---

## 📄 License

This project is licensed under the **MIT License** — see [LICENSE](LICENSE) for details.

---

<div align="center">

Made with ⚡ by [**Nexvir**](https://github.com/Nexvir)

*ReconRadar APOLLO v7.0 HACKER EDITION*

*Star ⭐ the repo if you find it useful!*

</div>
