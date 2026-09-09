# ReconRadar APOLLO v7.0 HACKER EDITION

## 🚀 Ultimate Security Reconnaissance & Penetration Testing Framework

![Version](https://img.shields.io/badge/version-7.0%20HACKER%20EDITION-00ff88)
![License](https://img.shields.io/badge/license-MIT-blue)
![Python](https://img.shields.io/badge/python-3.8+-blue)

---

## ✨ What's New in v7.0 HACKER EDITION

### 🔐 Hash Cracker Module
- **Multi-Algorithm Support**: MD5, SHA1, SHA256, SHA384, SHA512, NTLM, Base64
- **Attack Methods**: Dictionary, Rule-Based, Brute-Force
- **Database Integration**: Persistent storage of cracked passwords
- **Auto-Detection**: Automatic hash type identification
- **Web Interface**: Integrated UI tab for hash cracking operations

### 🗄️ Professional Database Layer
- **SQLAlchemy ORM**: SQLite (default) or PostgreSQL support
- **6 Core Tables**: Scans, Findings, Screenshots, Targets, APIKeys, Cache
- **Persistent Storage**: All scan results saved permanently
- **Advanced Queries**: Filter by severity, category, target
- **Statistics Dashboard**: Real-time analytics

### 🎯 Hacker Mode Enhancements
- **Advanced Subdomain Enumeration**: Permutation scanning + CT logs
- **Technology Fingerprinting**: Wappalyzer integration with CVE detection
- **Screenshot Capture**: Playwright-based web page screenshots
- **API Endpoint Discovery**: GraphQL, Swagger, REST APIs
- **Cloud Asset Discovery**: AWS S3, Azure Blob, GCP Storage
- **Credential Leak Detection**: GitHub dorking + breach databases
- **Vulnerability Correlation**: Attack chain analysis

### 🎨 Improved Dashboard
- **New Hash Cracker Tab**: Full-featured UI for password cracking
- **Statistics Panel**: Real-time metrics for all modules
- **History Viewer**: Browse previously cracked hashes
- **Enhanced Visual Design**: Cyberpunk aesthetic with improved UX

---

## 📁 Project Structure

```
/workspace/
├── backend.py           # Main FastAPI application (v7.0)
├── frontend.py          # HTML/CSS/JS dashboard
├── database.py          # SQLAlchemy ORM models & operations
├── hash_cracker.py      # Password hash cracking module
├── hacker_enhanced.py   # Advanced hacking features
├── reconradar.db        # SQLite database
├── data/                # Wordlists, signatures, configs
├── reports/             # HTML scan reports
├── screenshots/         # Captured web screenshots
└── requirements.txt     # Python dependencies
```

---

## 🚀 Quick Start

### Installation

```bash
# Install dependencies
pip install fastapi uvicorn python-nmap dnspython python-whois httpx sqlalchemy

# Optional: For advanced features
pip install python-Wappalyzer playwright
playwright install chromium

# Run the application
python backend.py
```

### Access the Dashboard

Open your browser and navigate to:
```
http://127.0.0.1:8000
```

---

## 🔧 API Endpoints

### Reconnaissance
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | Dashboard UI |
| WS | `/ws` | WebSocket for real-time scanning |
| GET | `/history` | List past scans |
| GET | `/history/{scan_id}` | View specific scan report |

### Hash Cracking
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/hash/crack` | Crack a password hash |
| GET | `/hash/history` | Get cracked hashes history |

### Statistics
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/stats` | System-wide statistics |

---

## 💻 Usage Examples

### 1. Start a Recon Scan

Via WebSocket (from dashboard):
```json
{
  "action": "start_scan",
  "target": "example.com",
  "nmap_args": "-sV -T4 -F -n",
  "modules": {
    "dns": true,
    "whois": true,
    "subdomain": true,
    "takeover": true,
    "web": true,
    "osint": true
  }
}
```

### 2. Crack a Hash

Via API:
```bash
curl -X POST http://127.0.0.1:8000/hash/crack \
  -H "Content-Type: application/json" \
  -d '{"hash": "5f4dcc3b5aa765d61d8327deb882cf99", "type": "MD5"}'
```

Response:
```json
{
  "success": true,
  "hash": "5f4dcc3b5aa765d61d83...",
  "hash_type": "MD5",
  "plaintext": "password",
  "method": "dictionary",
  "stats": {
    "total_attempted": 150,
    "total_cracked": 1,
    "time_elapsed": 0.002
  }
}
```

### 3. Get Statistics

```bash
curl http://127.0.0.1:8000/stats
```

---

## 🎯 Hash Cracker Features

### Supported Hash Types
- **MD5**: Fast, commonly used (vulnerable)
- **SHA-1**: Deprecated, collision attacks known
- **SHA-256**: Secure, widely adopted
- **SHA-384**: Extended security variant
- **SHA-512**: Maximum security in SHA-2 family
- **NTLM**: Windows password hashes
- **Base64**: Encoding (not a hash)

### Attack Methods

#### Dictionary Attack
- Uses built-in wordlist (150+ common passwords)
- Generates mutations (leet speak, numbers, special chars)
- Fast and effective for weak passwords

#### Rule-Based Attack
- Applies transformation rules to base words
- Common patterns: uppercase, reverse, append numbers
- Balanced speed/coverage

#### Brute-Force Attack
- Tries all character combinations
- Limited to 6 characters by default
- Slow but guaranteed (for short passwords)

### Database Storage
All cracked hashes are stored in `reconradar.db`:
- Hash value and type
- Plaintext result
- Cracking method used
- Timestamp
- Associated scan ID (if applicable)

---

## 🛡️ Hacker Mode Modules

### 1. Advanced Subdomain Enumeration
```python
from hacker_enhanced import advanced_subdomain_enum

subdomains = await advanced_subdomain_enum('target.com', ws, modules)
```

### 2. Technology Fingerprinting
```python
from hacker_enhanced import tech_stack_fingerprint

tech = await tech_stack_fingerprint('https://target.com')
# Returns: technologies, versions, potential vulnerabilities
```

### 3. Screenshot Capture
```python
from hacker_enhanced import capture_screenshot

await capture_screenshot('https://target.com', 'screenshots/target.png')
```

### 4. API Discovery
```python
from hacker_enhanced import api_endpoint_discovery

endpoints = await api_endpoint_discovery('target.com', ws)
```

### 5. Cloud Asset Discovery
```python
from hacker_enhanced import cloud_asset_discovery

assets = await cloud_asset_discovery('target.com', ws)
# Discovers: AWS S3, Azure Blob, GCP Storage
```

---

## 📊 Database Schema

### Tables
1. **scans**: Main scan sessions
2. **findings**: Individual results/findings
3. **screenshots**: Captured web pages
4. **targets**: Tracked targets over time
5. **api_keys**: Authentication keys
6. **cache**: DNS/WHOIS/Nmap cache
7. **cracked_hashes**: Password cracking results

### Query Examples
```python
from database import get_scan_history, get_statistics, get_cracked_hashes

# Get last 10 scans
scans = get_scan_history(limit=10)

# Get system stats
stats = get_statistics()

# Get cracked hashes
hashes = get_cracked_hashes(limit=50)
```

---

## ⚠️ Legal Disclaimer

**This tool is designed for authorized security testing and educational purposes only.**

- Only use on systems you own or have explicit permission to test
- Unauthorized access to computer systems is illegal
- The developers are not responsible for misuse of this software
- Always comply with local laws and regulations

---

## 🤝 Contributing

Contributions are welcome! Please feel free to submit issues and pull requests.

### Areas for Improvement
- [ ] Machine Learning vulnerability prediction
- [ ] Integration with Nessus/OpenVAS
- [ ] Dark Web monitoring
- [ ] Scheduled scans with webhooks
- [ ] PDF/Excel report export
- [ ] Multi-language support

---

## 📝 Changelog

### v7.0 HACKER EDITION (Current)
- ✅ Added Hash Cracker module with 7+ algorithms
- ✅ Integrated SQLAlchemy database layer
- ✅ Enhanced hacker mode with 6 new modules
- ✅ Improved dashboard with Hash Cracker tab
- ✅ Added statistics and history tracking
- ✅ Bug fixes and performance improvements

### v6.0 PRO
- Standalone HTML reports per scan
- Expanded OSINT sources (35+)
- DNS/WHOIS caching
- Rotating file logging

---

## 📧 Contact

- **GitHub**: [@Nexvir](https://github.com/Nexvir)
- **License**: MIT

---

**Made with ❤️ for the security community**
