# ReconRadar APOLLO v7.0 - Hacker Edition
## Professional Penetration Testing & Security Reconnaissance Platform

### 🚀 What's New in v7.0

#### **Database Layer (NEW)**
- ✅ Full SQLAlchemy ORM with SQLite/PostgreSQL support
- ✅ Persistent storage for scans, findings, and targets
- ✅ Advanced querying and reporting capabilities
- ✅ Target tracking over time with change detection
- ✅ API key authentication system
- ✅ Intelligent caching layer

#### **Hacker Mode Features (NEW)**
- 🔥 Advanced subdomain enumeration with permutation scanning
- 🔥 Technology stack fingerprinting (Wappalyzer integration)
- 🔥 Automated screenshot capture of web services
- 🔥 API endpoint discovery
- 🔥 Credential leak detection
- 🔥 Cloud asset discovery (AWS, Azure, GCP)
- 🔥 Vulnerability correlation and attack chain analysis

#### **Security Enhancements**
- 🛡️ Input validation to prevent SSRF and injection attacks
- 🛡️ Rate limiting per API key
- 🛡️ Secure credential handling
- 🛡️ Audit logging

---

## 📁 Project Structure

```
/workspace/
├── backend.py              # Main FastAPI application
├── frontend.py             # HTML/CSS/JS dashboard
├── database.py             # SQLAlchemy ORM models & operations
├── hacker_enhanced.py      # Advanced hacker mode modules
├── requirements.txt        # Python dependencies
├── data/                   # Configuration files
│   ├── wordlist.json       # Subdomain brute-force wordlist
│   ├── signatures.json     # Subdomain takeover signatures
│   ├── paths.txt           # Sensitive paths for scanning
│   └── osint.txt           # OSINT source URLs
├── reports/                # Generated HTML reports
├── screenshots/            # Captured website screenshots
└── reconradar.db           # SQLite database
```

---

## 🛠️ Installation

### Prerequisites
- Python 3.8+
- Nmap installed on system
- Git (optional, for cloning)

### Quick Install
```bash
cd /workspace
pip install -r requirements.txt

# Install additional dependencies for advanced features
pip install playwright
playwright install chromium
```

### Database Setup
The database auto-initializes on first run. For PostgreSQL:
```bash
export RECONRADAR_DB="postgresql://user:pass@localhost/reconradar"
```

---

## 🚀 Usage

### Start the Application
```bash
python backend.py
```

Access the dashboard at: `http://127.0.0.1:8000`

### Basic Scan via WebSocket
```javascript
const ws = new WebSocket('ws://127.0.0.1:8000/ws');
ws.onopen = () => {
    ws.send(JSON.stringify({
        action: 'start_scan',
        target: 'example.com',
        nmap_args: '-sV -T4 -A',
        modules: {
            dns: true,
            whois: true,
            subdomain: true,
            takeover: true,
            web: true,
            osint: true
        },
        scan_id: 'my_scan_001'
    }));
};
```

### Using Hacker Mode (Python)
```python
from hacker_enhanced import hacker_mode_scan
import asyncio

async def run_hacker_scan():
    # Create a mock WebSocket for testing
    class MockWS:
        async def send_text(self, msg):
            print(msg)
    
    ws = MockWS()
    await hacker_mode_scan(
        target='example.com',
        ws=ws,
        scan_id='hack_001',
        modules={'screenshots': True}
    )

asyncio.run(run_hacker_scan())
```

### Database Queries
```python
from database import *

# Get statistics
stats = get_statistics()
print(f"Total scans: {stats['total_scans']}")

# Get scan history
history = get_scan_history(limit=50)

# Get findings for a specific scan
findings = get_scan_findings('scan_id_123')

# Filter by category
vulns = get_scan_findings('scan_id_123', category='vuln')

# Track a target
target = get_or_create_target('example.com')
update_target_last_scanned('example.com')
```

---

## 📊 API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | GET | Web dashboard |
| `/ws` | WebSocket | Real-time scan communication |
| `/history` | GET | List all past scans |
| `/history/{scan_id}` | GET | View HTML report for scan |
| `/api/stats` | GET | System statistics |
| `/api/targets` | GET/POST | Manage tracked targets |
| `/api/findings` | GET | Query findings with filters |

---

## 🔧 Configuration

### Environment Variables
```bash
# Database connection
RECONRADAR_DB=sqlite:///reconradar.db
# or
RECONRADAR_DB=postgresql://user:pass@localhost/reconradar

# Rate limiting
RATE_LIMIT_PER_HOUR=100

# Screenshot settings
SCREENSHOT_TIMEOUT=30000
SCREENSHOT_WIDTH=1920
SCREENSHOT_HEIGHT=1080
```

### Custom Wordlists
Edit `data/wordlist.json` to add custom subdomain prefixes.

### Custom Takeover Signatures
Edit `data/signatures.json` to add cloud service takeover signatures.

Format: `[["signature_pattern", "Service Name", "Exploitation Steps"]]`

---

## 🎯 Hacker Mode Modules

### 1. Advanced Subdomain Enumeration
- Certificate Transparency logs
- DNS brute-force with permutations
- Search engine dorking
- Public dataset mining

### 2. Technology Fingerprinting
- Wappalyzer integration
- Version detection
- Known vulnerability mapping
- CVE correlation

### 3. Screenshot Capture
- Full-page screenshots
- Multiple viewport sizes
- Automatic thumbnail generation

### 4. API Discovery
- Common endpoint enumeration
- Swagger/OpenAPI detection
- GraphQL endpoint finding
- JavaScript analysis

### 5. Cloud Asset Discovery
- AWS S3 bucket detection
- Azure Blob Storage
- GCP Cloud Storage
- CloudFront/CDN identification

### 6. Credential Leak Detection
- GitHub code search
- Breach database queries
- Paste site monitoring

### 7. Vulnerability Correlation
- Attack chain identification
- Risk prioritization
- Exploit suggestions (educational)

---

## 📈 Performance Optimization

The database uses several optimizations:
- WAL mode for SQLite
- Connection pooling
- Indexed queries
- Batch insert operations
- Cache layer for DNS/WHOIS

---

## ⚠️ Legal Disclaimer

**ReconRadar APOLLO is designed for authorized security testing only.**

- Only use against systems you own or have explicit permission to test
- The authors are not responsible for misuse
- Comply with all applicable laws and regulations
- This tool is for educational and professional security research

---

## 🤝 Contributing

Contributions welcome! Areas for improvement:
- Additional OSINT sources
- More cloud provider support
- Machine learning for vulnerability prediction
- Integration with vulnerability scanners (Nessus, OpenVAS)
- Dark web monitoring integration

---

## 📄 License

MIT License - See LICENSE file for details

---

## 🙏 Credits

Created by github.com/Nexvir

Special thanks to the open-source community for:
- FastAPI
- SQLAlchemy
- Wappalyzer
- Playwright
- python-nmap

---

**Version:** 7.0.0  
**Last Updated:** 2024  
**GitHub:** https://github.com/Nexvir/reconradar
