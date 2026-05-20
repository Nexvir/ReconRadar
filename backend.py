"""
ReconRadar APOLLO v6.0 - Backend
----------------------------------
GitHub : https://github.com/Nexvir
Run    : python backend.py

What's in this file:
  • All imports + RotatingFileHandler logging (reconradar.log)
  • JSON-based persistence (data/wordlist.json, data/signatures.json)
  • HTML report per scan saved to reports/{scan_id}.html
  • In-memory DNS cache (TTL 300 s) and WHOIS cache (TTL 24 h)
  • ConnectionManager with per-scan result buffering
  • All recon modules (DNS/WHOIS, crt.sh, subdomain brute-force,
    takeover verification, HTTP probe, HTTP vuln scan, OSINT, nmap)
  • FastAPI app + WebSocket /ws + GET / (HTML dashboard)
  • REST endpoints:
      GET  /history               – list of past scan reports
      GET  /history/{scan_id}     – open the HTML report for one scan
  • HTML_TEMPLATE imported from frontend.py

Dependencies:
  pip install fastapi uvicorn python-nmap dnspython python-whois httpx
  System: Nmap must be installed. Root/Admin for -sS / -O / -f scans.
"""

import asyncio
import json
import os
import re
import socket
import ssl
import time
import random
import logging
import logging.handlers
import urllib.request
import urllib.error
from contextlib import contextmanager
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Any, Set, Optional, Tuple

from fastapi import FastAPI, WebSocket, WebSocketDisconnect, HTTPException, Header
from fastapi.responses import HTMLResponse, JSONResponse
import uvicorn

# ── Optional heavy deps ─────────────────────────────────────────────────────

try:
    import httpx
    HTTPX_AVAILABLE = True
except ImportError:
    HTTPX_AVAILABLE = False

try:
    import nmap
    NMAP_AVAILABLE = True
except ImportError:
    NMAP_AVAILABLE = False

try:
    import dns.resolver
    import dns.zone
    import dns.query
    DNS_AVAILABLE = True
except ImportError:
    DNS_AVAILABLE = False

try:
    import whois
    WHOIS_AVAILABLE = True
except ImportError:
    WHOIS_AVAILABLE = False

import warnings
warnings.filterwarnings("ignore", message="Unverified HTTPS request")
warnings.filterwarnings("ignore", category=DeprecationWarning)

# ── Logging setup ────────────────────────────────────────────────────────────

_log_file_handler = logging.handlers.RotatingFileHandler(
    "reconradar.log", maxBytes=10 * 1024 * 1024, backupCount=5, encoding="utf-8"
)
_log_file_handler.setFormatter(
    logging.Formatter("%(asctime)s [%(levelname)s] %(name)s: %(message)s")
)
_log_console_handler = logging.StreamHandler()
_log_console_handler.setFormatter(
    logging.Formatter("%(asctime)s [%(levelname)s] %(name)s: %(message)s")
)
logging.basicConfig(level=logging.INFO, handlers=[_log_file_handler, _log_console_handler])
logger = logging.getLogger("ReconRadar")

# ── Frontend template ────────────────────────────────────────────────────────

from frontend import HTML_TEMPLATE

# ═══════════════════════════════════════════════════════════════════════════
# STORAGE PATHS
# ═══════════════════════════════════════════════════════════════════════════

DATA_DIR    = Path("data")
REPORTS_DIR = Path("reports")
WORDLIST_FILE    = DATA_DIR / "wordlist.json"
SIGNATURES_FILE  = DATA_DIR / "signatures.json"
INDEX_FILE       = REPORTS_DIR / "index.json"

# ── Default takeover signatures ──────────────────────────────────────────────

TAKEOVER_SIGNATURES_DEFAULT: List[Tuple[str, str, str]] = [
    ("cloudfront.net",          "CloudFront",               "Create CloudFront distribution with matching origin"),
    ("s3.amazonaws.com",        "AWS S3 Bucket",            "Create S3 bucket with exact name"),
    ("s3-website",              "AWS S3 Website",           "Create S3 static website hosting"),
    ("elasticbeanstalk.com",    "AWS Elastic Beanstalk",    "Deploy Elastic Beanstalk app"),
    ("herokuapp.com",           "Heroku",                   "Deploy Heroku app with the subdomain name"),
    ("netlify.app",             "Netlify",                  "Add site in Netlify dashboard"),
    ("netlify.com",             "Netlify (legacy)",         "Add site in Netlify dashboard"),
    ("pages.dev",               "Cloudflare Pages",         "Create Cloudflare Pages project"),
    ("azureedge.net",           "Azure CDN",                "Create Azure CDN endpoint profile"),
    ("trafficmanager.net",      "Azure Traffic Manager",    "Create Azure TM profile"),
    ("azurewebsites.net",       "Azure App Service",        "Create Azure Web App"),
    ("azure-api.net",           "Azure API Management",     "Create Azure API Management instance"),
    ("cloudapp.net",            "Azure Cloud Services",     "Create Azure Cloud Service"),
    ("pantheon.io",             "Pantheon",                 "Create Pantheon site"),
    ("pantheonsite.io",         "Pantheon (legacy)",        "Create Pantheon site"),
    ("github.io",               "GitHub Pages",             "Create a GitHub Pages repo with matching CNAME file"),
    ("gitlab.io",               "GitLab Pages",             "Create GitLab Pages site"),
    ("bitbucket.io",            "Bitbucket Cloud",          "Create Bitbucket Pipelines site"),
    ("firebaseapp.com",         "Firebase",                 "Create Firebase project"),
    ("web.app",                 "Firebase (web)",           "Create Firebase project"),
    ("vercel.app",              "Vercel",                   "Deploy Vercel project"),
    ("vercel.com",              "Vercel (legacy)",          "Deploy Vercel project"),
    ("onrender.com",            "Render",                   "Create Render service"),
    ("fly.dev",                 "Fly.io",                   "Deploy Fly.io app"),
    ("surge.sh",                "Surge",                    "Deploy to Surge.sh"),
    ("myshopify.com",           "Shopify",                  "Create Shopify store with that name"),
    ("shopify.com",             "Shopify (custom)",         "Create Shopify store"),
    ("zendesk.com",             "Zendesk",                  "Create Zendesk subdomain"),
    ("freshdesk.com",           "Freshdesk",                "Create Freshdesk subdomain"),
    ("freshservice.com",        "Freshservice",             "Create Freshservice subdomain"),
    ("helpscout.net",           "Help Scout",               "Create Help Scout docs"),
    ("helpjuice.com",           "Helpjuice",                "Create Helpjuice KB"),
    ("ghost.io",                "Ghost",                    "Create Ghost blog"),
    ("ghost.org",               "Ghost (self)",             "Create Ghost blog"),
    ("readme.io",               "ReadMe",                   "Create ReadMe docs site"),
    ("readthedocs.io",          "Read the Docs",            "Create Read the Docs project"),
    ("unbouncepages.com",       "Unbounce",                 "Create Unbounce landing page"),
    ("statuspage.io",           "Statuspage",               "Create Statuspage page"),
    ("atlassian.net",           "Atlassian",                "Create Jira/Confluence site"),
    ("000webhostapp.com",       "000WebHost",               "Create free hosting account"),
    ("cargo.site",              "Cargo",                    "Create Cargo site"),
    ("tilda.ws",                "Tilda",                    "Create Tilda site"),
    ("ucraft.net",              "Ucraft",                   "Create Ucraft site"),
    ("hatchbox.io",             "Hatchbox",                 "Deploy Hatchbox app"),
    ("fastly.net",              "Fastly",                   "Configure Fastly service"),
    ("strikingly.com",          "Strikingly",               "Create Strikingly site"),
    ("hostingerapp.com",        "Hostinger",                "Create Hostinger site"),
    ("flywheelsites.com",       "Flywheel",                 "Create Flywheel site"),
    ("kinsta.com",              "Kinsta",                   "Create Kinsta site"),
    ("wpengine.com",            "WP Engine",                "Create WP Engine site"),
    ("wpenginepowered.com",     "WP Engine (legacy)",       "Create WP Engine site"),
    ("liquidweb.com",           "Liquid Web",               "Create Liquid Web site"),
]

DEFAULT_WORDLIST: List[str] = [
    'www', 'mail', 'remote', 'blog', 'webmail', 'api', 'dev', 'staging',
    'test', 'admin', 'portal', 'vpn', 'ftp', 'ssh', 'git', 'jenkins',
    'jira', 'confluence', 'wiki', 'cdn', 'support', 'help', 'forum',
    'shop', 'store', 'm', 'app', 'mobile', 'ns1', 'ns2', 'mx',
    'smtp', 'pop3', 'imap', 'calendar', 'owa', 'exchange', 'cpanel',
    'whm', 'phpmyadmin', 'mysql', 'db', 'database', 'static', 'assets',
    'images', 'img', 'video', 'media', 'download', 'files', 'cloud',
    'backup', 'secure', 'login', 'register', 'signup', 'status',
    'docs', 'documentation', 'developer', 'statuspage', 'grafana',
    'prometheus', 'kibana', 'elastic', 'logs', 'monitor', 'monitoring',
    'dashboard', 'analytics', 'stats', 'metrics', 'graphql', 'swagger',
    'api-docs', 'redoc', 'hook', 'webhook', 'notification', 'notify',
    'track', 'tracking', 'collector', 'events', 'socket',
    'ws', 'wss', 'chat', 'talk', 'team', 'slack', 'discord', 'matrix',
    'labs', 'beta', 'alpha', 'prod', 'production', 'stage', 'sandbox',
    'demo', 'playground', 'internal', 'corp', 'hr', 'payroll',
    'pay', 'payment', 'billing', 'invoice', 'checkout', 'cart',
    'sso', 'auth', 'identity', 'oauth',
    'autodiscover', 'lyncdiscover', 'sip', 'meet', 'zoom', 'teams',
    'remoteaccess', 'rdp', 'citrix', 'horizon', 'vdi', 'vcenter',
    'docker', 'k8s', 'kubernetes', 'cluster', 'node', 'worker',
    'registry', 'harbor', 'nexus', 'artifactory',
    'sonar', 'sonarqube', 'ci', 'cd', 'build', 'runner', 'pipeline',
    'bamboo', 'teamcity', 'circleci', 'travis', 'argocd',
    'kafka', 'rabbitmq', 'redis', 'memcached', 'haproxy', 'nginx',
    'ses', 'sns', 'sqs', 'lambda', 'functions', 'serverless',
    'adminer', 'phpadmin', 'admin-console', 'management',
    'partner', 'partners', 'vendor', 'vendors', 'wholesale',
    'esxi', 'vmware', 'proxmox', 'npm', 'pypi', 'maven',
    'proxy', 'reverse-proxy', 'gateway', 'api-gateway',
    'mailgun', 'sendgrid', 'mailchimp', 'postmark',
]

# ═══════════════════════════════════════════════════════════════════════════
# JSON-BASED STORAGE
# ═══════════════════════════════════════════════════════════════════════════

def init_storage():
    """Create required directories and seed JSON files if they don't exist."""
    DATA_DIR.mkdir(exist_ok=True)
    REPORTS_DIR.mkdir(exist_ok=True)

    if not WORDLIST_FILE.exists():
        WORDLIST_FILE.write_text(
            json.dumps(DEFAULT_WORDLIST, indent=2, ensure_ascii=False),
            encoding="utf-8"
        )
        logger.info("Seeded wordlist.json with %d words", len(DEFAULT_WORDLIST))

    if not SIGNATURES_FILE.exists():
        data = [list(s) for s in TAKEOVER_SIGNATURES_DEFAULT]
        SIGNATURES_FILE.write_text(
            json.dumps(data, indent=2, ensure_ascii=False),
            encoding="utf-8"
        )
        logger.info("Seeded signatures.json with %d entries", len(data))

    if not INDEX_FILE.exists():
        INDEX_FILE.write_text("[]", encoding="utf-8")

    _paths_txt = DATA_DIR / "paths.txt"
    if not _paths_txt.exists():
        _paths_txt.write_text(
            "# Add sensitive paths here, one per line\n",
            encoding="utf-8",
        )
        logger.info("Created placeholder data/paths.txt")

    _subdomains_txt = DATA_DIR / "subdomains.txt"
    if not _subdomains_txt.exists():
        _subdomains_txt.write_text(
            "# Add subdomain words here, one per line\n",
            encoding="utf-8",
        )
        logger.info("Created placeholder data/subdomains.txt")

    _osint_txt = DATA_DIR / "osint.txt"
    if not _osint_txt.exists():
        _osint_txt.write_text(
            "# Format: SourceName | Type | https://url/{target}\n",
            encoding="utf-8",
        )
        logger.info("Created placeholder data/osint.txt")


def _load_wordlist() -> List[str]:
    """Load wordlist from JSON file, fallback to default."""
    try:
        data = json.loads(WORDLIST_FILE.read_text(encoding="utf-8"))
        if isinstance(data, list) and data:
            return [str(w) for w in data]
    except Exception:
        pass
    return DEFAULT_WORDLIST


def _load_signatures() -> List[Tuple[str, str, str]]:
    """Load takeover signatures from JSON file, fallback to default."""
    try:
        data = json.loads(SIGNATURES_FILE.read_text(encoding="utf-8"))
        if isinstance(data, list) and data:
            return [(row[0], row[1], row[2]) for row in data if len(row) >= 3]
    except Exception:
        pass
    return TAKEOVER_SIGNATURES_DEFAULT


def _index_upsert(scan_id: str, target: str, start_time: str,
                  status: str, end_time: str = ""):
    """Add or update a scan entry in the index file."""
    try:
        index = json.loads(INDEX_FILE.read_text(encoding="utf-8"))
    except Exception:
        index = []

    for entry in index:
        if entry.get("id") == scan_id:
            entry["status"]   = status
            entry["end_time"] = end_time
            break
    else:
        index.insert(0, {
            "id":         scan_id,
            "target":     target,
            "start_time": start_time,
            "end_time":   end_time,
            "status":     status,
            "report":     f"{scan_id}.html",
        })

    INDEX_FILE.write_text(
        json.dumps(index, indent=2, ensure_ascii=False),
        encoding="utf-8"
    )


def _save_html_report(scan_id: str, target: str, start_time: str,
                      results: List[Dict]):
    """Generate and save a styled HTML report for one scan."""

    def esc(s: str) -> str:
        return str(s or "").replace("&", "&amp;").replace("<", "&lt;") \
                           .replace(">", "&gt;").replace('"', "&quot;")

    def sev_color(s: str) -> str:
        u = (s or "").upper()
        if u == "HIGH":   return "#ff3355"
        if u == "MEDIUM": return "#ff7b00"
        if u == "LOW":    return "#ffd60a"
        if u.startswith("2"): return "#00e676"
        if u.startswith("3"): return "#00cfff"
        if u.startswith("4"): return "#ff7b00"
        if u.startswith("5"): return "#ff3355"
        return "#6080a0"

    cats = {
        "dns":   {"label": "DNS Records",      "cols": ["ASSET",   "TYPE",   "DETAILS",  "INFO"]},
        "sub":   {"label": "Subdomains",        "cols": ["SUBDOMAIN","SOURCE","IP/CNAME", "STATUS"]},
        "port":  {"label": "Open Ports",        "cols": ["HOST:PORT","STATE", "SERVICE",  "RISK"]},
        "web":   {"label": "Web Services",      "cols": ["URL",     "STATUS","TECH/HDR",  "WAF"]},
        "vuln":  {"label": "Vulnerabilities",   "cols": ["TARGET",  "THREAT","DETAILS",   "SEVERITY"]},
        "osint": {"label": "OSINT Links",       "cols": ["SOURCE",  "TYPE",  "LINK",      "INFO"]},
    }

    grouped: Dict[str, List[Dict]] = {k: [] for k in cats}
    for r in results:
        cat = r.get("category", "dns")
        if cat in grouped:
            grouped[cat].append(r)

    summary_parts = []
    total = 0
    for k, info in cats.items():
        n = len(grouped[k])
        total += n
        summary_parts.append(
            f'<span style="color:#00cfff">{info["label"]}</span>: '
            f'<b style="color:#fff">{n}</b>'
        )
    summary_html = " &nbsp;|&nbsp; ".join(summary_parts)

    sections_html = ""
    for cat, info in cats.items():
        rows = grouped[cat]
        if not rows:
            continue
        tbody = ""
        for r in rows:
            c3 = esc(r.get("col3", ""))
            if cat == "osint" and str(r.get("col3", "")).startswith("http"):
                c3 = f'<a href="{esc(r.get("col3",""))}" target="_blank" style="color:#00cfff">{esc(r.get("col3",""))}</a>'
            sev = r.get("severity", "Info")
            tbody += (
                f'<tr>'
                f'<td>{esc(r.get("col1",""))}</td>'
                f'<td>{esc(r.get("col2",""))}</td>'
                f'<td>{c3}</td>'
                f'<td style="color:{sev_color(sev)};font-weight:bold">{esc(sev)}</td>'
                f'</tr>'
            )
        sections_html += f"""
<h2 style="color:#00cfff;margin:28px 0 8px;font-size:13px;letter-spacing:.15em;
           text-transform:uppercase;border-bottom:1px solid #112030;padding-bottom:6px">
  {info["label"]}
  <span style="color:#6080a0;font-size:11px">({len(rows)} items)</span>
</h2>
<table style="width:100%;border-collapse:collapse;font-size:11px;font-family:'Courier New',monospace">
  <thead><tr>{''.join(f'<th style="padding:6px 10px;text-align:left;color:#005a7a;font-size:9px;letter-spacing:.18em;border-bottom:1px solid #112030">{c}</th>' for c in info["cols"])}</tr></thead>
  <tbody>{tbody}</tbody>
</table>
"""

    end_time = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC")
    report_html = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>ReconRadar Report — {esc(target)}</title>
  <style>
    *{{box-sizing:border-box;margin:0;padding:0}}
    body{{background:#040810;color:#6080a0;font-family:'Courier New',monospace;
         font-size:12px;padding:30px;line-height:1.6}}
    table td{{padding:6px 10px;border-bottom:1px solid #0a1220;
              vertical-align:top;word-break:break-word;max-width:340px}}
    table tr:hover td{{background:rgba(0,207,255,.03)}}
    a{{color:#00cfff;text-decoration:none}} a:hover{{text-decoration:underline}}
    .header{{border:1px solid #112030;padding:20px 24px;margin-bottom:24px;background:#070d16}}
  </style>
</head>
<body>
<div class="header">
  <div style="color:#00cfff;font-size:16px;font-weight:bold;letter-spacing:.1em;margin-bottom:6px">
    &#128737; ReconRadar APOLLO v6.0 — Intelligence Report
  </div>
  <div style="color:#b0c8e0;margin-bottom:4px">
    Target: <b style="color:#fff">{esc(target)}</b>
    &nbsp;&nbsp;|&nbsp;&nbsp;
    Scan ID: <span style="color:#6080a0">{esc(scan_id)}</span>
  </div>
  <div style="color:#6080a0;font-size:10px;margin-bottom:10px">
    Started: {esc(start_time)} &nbsp;|&nbsp; Saved: {end_time}
  </div>
  <div style="font-size:11px">
    Total findings: <b style="color:#fff">{total}</b>
    &nbsp;&nbsp;|&nbsp;&nbsp; {summary_html}
  </div>
</div>

{sections_html}

<div style="margin-top:30px;color:#253a52;font-size:10px;text-align:center">
  ReconRadar APOLLO v6.0 &mdash; github.com/Nexvir &mdash; For authorized security testing only
</div>
</body>
</html>
"""
    report_path = REPORTS_DIR / f"{scan_id}.html"
    report_path.write_text(report_html, encoding="utf-8")
    logger.info("Saved HTML report: %s (%d findings)", report_path, total)


# ═══════════════════════════════════════════════════════════════════════════
# CACHING
# ═══════════════════════════════════════════════════════════════════════════

_dns_cache:   Dict[str, Tuple[Any, float]] = {}
_whois_cache: Dict[str, Tuple[Any, float]] = {}
DNS_CACHE_TTL   = 300
WHOIS_CACHE_TTL = 86400


def _cache_get(store: dict, key: str, ttl: float):
    entry = store.get(key)
    if entry and (time.time() - entry[1]) < ttl:
        return entry[0]
    return None


def _cache_set(store: dict, key: str, value):
    store[key] = (value, time.time())


# ═══════════════════════════════════════════════════════════════════════════
# FASTAPI APP
# ═══════════════════════════════════════════════════════════════════════════

app = FastAPI(title="ReconRadar APOLLO v6.0 by github.com/Nexvir", version="6.0.0")


# ═══════════════════════════════════════════════════════════════════════════
# CONNECTION MANAGER
# ═══════════════════════════════════════════════════════════════════════════

class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []
        self.scan_tasks: Dict[str, asyncio.Task] = {}
        self._ws_scan_id: Dict[int, str] = {}
        self._scan_buffers: Dict[str, List[Dict]] = {}

    async def connect(self, ws: WebSocket):
        await ws.accept()
        self.active_connections.append(ws)

    def disconnect(self, ws: WebSocket):
        self._ws_scan_id.pop(id(ws), None)
        if ws in self.active_connections:
            self.active_connections.remove(ws)

    def start_scan_buffer(self, ws: WebSocket, scan_id: str):
        self._ws_scan_id[id(ws)] = scan_id
        self._scan_buffers[scan_id] = []

    def get_scan_buffer(self, scan_id: str) -> List[Dict]:
        return self._scan_buffers.get(scan_id, [])

    def clear_scan_buffer(self, scan_id: str):
        self._scan_buffers.pop(scan_id, None)

    async def log(self, ws: WebSocket, msg: str):
        try:
            await ws.send_text(json.dumps({"type": "log", "data": msg}))
        except Exception:
            pass

    async def result(self, ws: WebSocket, col1: str, col2: str, col3: str,
                     severity: str = "Info", category: str = "dns"):
        data = {"col1": col1, "col2": col2, "col3": col3,
                "severity": severity, "category": category}
        try:
            await ws.send_text(json.dumps({"type": "result", "data": data}))
        except Exception:
            pass
        scan_id = self._ws_scan_id.get(id(ws))
        if scan_id and scan_id in self._scan_buffers:
            self._scan_buffers[scan_id].append(data)

    async def status(self, ws: WebSocket, s: str):
        try:
            await ws.send_text(json.dumps({"type": "status", "data": s}))
        except Exception:
            pass


manager = ConnectionManager()


# ═══════════════════════════════════════════════════════════════════════════
# COMMON PORTS
# ═══════════════════════════════════════════════════════════════════════════

COMMON_PORTS = [
    21, 22, 23, 25, 53, 80, 110, 111, 135, 139, 143, 443, 445,
    465, 587, 993, 995, 1433, 1521, 2049, 2375, 2376, 3000, 3306,
    3389, 4443, 5000, 5432, 5900, 6379, 6443, 7001, 7443, 8000,
    8080, 8081, 8443, 8888, 9000, 9090, 9200, 9300, 9443, 10000,
    11211, 27017, 28017, 50070,
]


# ═══════════════════════════════════════════════════════════════════════════
# TAKEOVER VERIFICATION
# ═══════════════════════════════════════════════════════════════════════════

async def verify_takeover(domain: str, cname: str) -> Tuple[bool, str, str]:
    if not DNS_AVAILABLE or not HTTPX_AVAILABLE:
        return False, "DNS/HTTPX unavailable", ""

    signatures = _load_signatures()
    cname_lower = cname.lower()
    matched_service = "Unknown"
    for sig, svc, _ in signatures:
        if sig in cname_lower:
            matched_service = svc
            break

    try:
        dns.resolver.resolve(cname, 'A', lifetime=3)
        cname_resolves = True
    except Exception:
        cname_resolves = False

    if not cname_resolves:
        return True, f"DNS NXDOMAIN - CNAME '{cname}' does not resolve", matched_service

    try:
        async with httpx.AsyncClient(verify=False, timeout=8.0, follow_redirects=True) as client:
            for scheme in ('https', 'http'):
                url = f"{scheme}://{domain}"
                try:
                    resp = await client.get(url, headers={'User-Agent': 'Mozilla/5.0 (ReconRadar APOLLO)'})
                    status = resp.status_code
                    text   = (resp.text or "").lower()
                    headers = str(resp.headers).lower()
                    server  = resp.headers.get('server', '').lower()

                    if "no such bucket" in text or "bucket does not exist" in text:
                        return True, f"AWS S3: 'No Such Bucket' (HTTP {status})", matched_service
                    if "the specified bucket does not exist" in text:
                        return True, f"AWS S3: bucket missing (HTTP {status})", matched_service
                    if "cloudfront" in server or "cloudfront" in headers:
                        if status in (403, 404) and "error" in text and "request" in text:
                            return True, f"CloudFront: distribution error (HTTP {status})", matched_service
                        if status in (200, 301, 302):
                            return False, f"CloudFront active (HTTP {status})", matched_service
                    if "github" in server or "github" in headers:
                        if "repository not found" in text or "there isn't a github pages site here" in text:
                            return True, f"GitHub Pages: repo missing (HTTP {status})", matched_service
                        if status == 200:
                            return False, "GitHub Pages active", matched_service
                    if "heroku" in server or "heroku" in text:
                        if "no such app" in text or "there's nothing here" in text:
                            return True, f"Heroku: app not found (HTTP {status})", matched_service
                        if status == 200:
                            return False, "Heroku active", matched_service
                    if "netlify" in server or "netlify" in headers:
                        if "page not found" in text and "netlify" in text:
                            return True, f"Netlify: site not found (HTTP {status})", matched_service
                        if status == 200:
                            return False, "Netlify active", matched_service
                    if status == 404:
                        if "azure" in text or "azure" in headers:
                            return True, f"Azure: resource not found (HTTP 404)", matched_service
                        if "fastly" in text or "fastly" in headers:
                            return False, "Fastly active (404 expected)", matched_service
                        return True, f"HTTP 404 Not Found on cloud platform", matched_service
                    if status in (200, 301, 302, 307, 308):
                        return False, f"Service active (HTTP {status})", matched_service
                    break
                except httpx.ConnectError:
                    return True, f"Connection refused on {scheme} - no active service", matched_service
                except Exception:
                    continue
    except Exception:
        return False, "DNS resolves but HTTP probe failed", matched_service

    return False, "CNAME resolves and no takeover indicators found", matched_service


# ═══════════════════════════════════════════════════════════════════════════
# NMAP WRAPPER
# ═══════════════════════════════════════════════════════════════════════════

def _is_root() -> bool:
    try:
        return os.geteuid() == 0
    except AttributeError:
        try:
            import ctypes
            return ctypes.windll.shell32.IsUserAnAdmin() != 0
        except Exception:
            return False


def run_nmap_scan(target_ip: str, nmap_args: str) -> Tuple[List[Dict[str, Any]], str]:
    if not NMAP_AVAILABLE:
        raise RuntimeError("python-nmap not available")
    if not nmap_args.strip():
        nmap_args = "-sV -T4 -F -Pn -n"

    warning = ""
    root_flags = {'-sS', '-sF', '-sX', '-sN', '-sA', '-O', '-f'}
    needs_root = any(flag in nmap_args.split() for flag in root_flags)

    if needs_root and not _is_root():
        original = nmap_args
        nmap_args = nmap_args.replace('-sS', '-sT')
        for flag in ('-sF', '-sX', '-sN', '-sA', '-O', '-f'):
            nmap_args = nmap_args.replace(flag, '')
        nmap_args = ' '.join(nmap_args.split())
        warning = (
            f"[NMAP] ⚠ Not root — switched to TCP Connect scan (-sT). "
            f"Original: {original} → Effective: {nmap_args}. "
            f"Run with sudo for SYN/OS-detection."
        )

    nm = nmap.PortScanner()
    nm.scan(target_ip, arguments=nmap_args)

    results = []
    for host in nm.all_hosts():
        host_info = nm[host]
        os_name = "Unknown"
        if 'osmatch' in host_info and host_info['osmatch']:
            os_name = host_info['osmatch'][0].get('name', 'Unknown')
        for proto in host_info.all_protocols():
            for port in sorted(host_info[proto].keys()):
                info = host_info[proto][port]
                svc = info.get('name', 'unknown')
                product = info.get('product', '')
                version = info.get('version', '')
                extrainfo = info.get('extrainfo', '')
                parts = []
                if product:   parts.append(product)
                if version:   parts.append(version)
                if extrainfo: parts.append(f"({extrainfo})")
                svc_str = svc
                if parts:           svc_str += f" → {' '.join(parts)}"
                if os_name != "Unknown": svc_str += f" | OS: {os_name}"
                script_output = {}
                if 'script' in info:
                    script_output = dict(info['script'])
                    keys = list(script_output.keys())
                    if keys:
                        svc_str += f" | Scripts: {', '.join(keys[:3])}"
                results.append({
                    "host": host, "port": port, "protocol": proto,
                    "state": info.get('state', 'unknown'),
                    "service": svc_str[:200], "scripts": script_output,
                })
    return results, warning


# ═══════════════════════════════════════════════════════════════════════════
# SOCKET FALLBACK PORT SCANNER
# ═══════════════════════════════════════════════════════════════════════════

def socket_port_scan(target_ip: str, ports: List[int],
                     timeout: float = 1.0) -> List[Dict[str, Any]]:
    results = []
    for port in ports:
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.settimeout(timeout)
                ret = s.connect_ex((target_ip, port))
                if ret == 0:
                    banner = ""
                    try:
                        s.sendall(b"HEAD / HTTP/1.0\r\n\r\n")
                        raw = s.recv(256)
                        banner = raw.decode(errors='ignore').split('\n')[0].strip()[:80]
                    except Exception:
                        pass
                    results.append({
                        "host": target_ip, "port": port, "protocol": "tcp",
                        "state": "open", "service": banner or "unknown", "scripts": {},
                    })
        except Exception:
            pass
    return results


# ═══════════════════════════════════════════════════════════════════════════
# DNS ZONE TRANSFER
# ═══════════════════════════════════════════════════════════════════════════

async def dns_zone_transfer(target: str, websocket: WebSocket):
    if not DNS_AVAILABLE:
        return
    await manager.log(websocket, "[DNS-ZONE] Checking for zone transfer vulnerability...")
    try:
        ns_answers = dns.resolver.resolve(target, 'NS', lifetime=5)
        nameservers = [str(rdata).rstrip('.') for rdata in ns_answers]
        for ns in nameservers:
            try:
                ns_ip = socket.gethostbyname(ns)
                zone = dns.zone.from_xfr(dns.query.xfr(ns_ip, target, timeout=5, lifetime=10))
                if zone:
                    records = list(zone.nodes.keys())[:20]
                    detail = f"ZONE TRANSFER SUCCESSFUL via {ns} ({ns_ip})! Records: {', '.join(str(r) for r in records)}"
                    await manager.log(websocket, f"[!!!] ZONE TRANSFER: {target} is vulnerable via {ns}!")
                    await manager.result(websocket, target, "Zone Transfer", detail, "High", "vuln")
                    return
            except Exception:
                pass
        await manager.log(websocket, "[DNS-ZONE] Zone transfer not available (good security).")
    except Exception:
        pass


# ═══════════════════════════════════════════════════════════════════════════
# WHOIS + DNS MODULE
# ═══════════════════════════════════════════════════════════════════════════

async def dns_whois_module(target: str, ws: WebSocket, modules: dict):
    if modules.get('whois') and WHOIS_AVAILABLE:
        await manager.log(ws, "[WHOIS] Fetching domain registration (10 s timeout)...")
        try:
            cached = _cache_get(_whois_cache, target, WHOIS_CACHE_TTL)
            if cached:
                await manager.log(ws, "[WHOIS] (from cache)")
                await manager.result(ws, target, "WHOIS", cached, "Info", "dns")
            else:
                w = await asyncio.wait_for(
                    asyncio.to_thread(whois.whois, target), timeout=10.0
                )
                registrar = w.registrar or "Unknown"
                created   = w.creation_date
                expires   = w.expiration_date
                if isinstance(created, list): created = created[0]
                if isinstance(expires, list): expires = expires[0]
                org = getattr(w, 'org', '') or ''
                created_str = str(created)[:10] if created else 'N/A'
                expires_str = str(expires)[:10] if expires else 'N/A'
                details = f"Registrar: {registrar} | Created: {created_str} | Expires: {expires_str}"
                if org: details += f" | Org: {org}"
                _cache_set(_whois_cache, target, details)
                await manager.log(ws, f"[WHOIS] Complete - Registrar: {registrar}")
                await manager.result(ws, target, "WHOIS", details, "Info", "dns")
        except asyncio.TimeoutError:
            await manager.log(ws, "[WARN] WHOIS timeout (10 s). Skipping.")
            await manager.result(ws, target, "WHOIS", "WHOIS lookup timed out", "Info", "dns")
        except Exception as e:
            err_msg = str(e)[:100]
            await manager.log(ws, f"[WARN] WHOIS failed: {err_msg}")
            await manager.result(ws, target, "WHOIS", f"Lookup failed: {err_msg}", "Info", "dns")
    elif modules.get('whois') and not WHOIS_AVAILABLE:
        await manager.log(ws, "[WARN] WHOIS module unavailable (python-whois not installed)")

    if modules.get('dns') and DNS_AVAILABLE:
        await manager.log(ws, "[DNS] Enumerating DNS records (MX, TXT, NS, SOA, CNAME)...")
        count = 0
        for rtype in ['MX', 'TXT', 'NS', 'SOA', 'CNAME']:
            try:
                cache_key = f"{target}:{rtype}"
                cached_answers = _cache_get(_dns_cache, cache_key, DNS_CACHE_TTL)
                if cached_answers is None:
                    answers = dns.resolver.resolve(target, rtype, lifetime=4)
                    cached_answers = [str(rdata).replace('\n', ' ')[:150] for rdata in answers]
                    _cache_set(_dns_cache, cache_key, cached_answers)
                for txt in cached_answers:
                    await manager.result(ws, target, rtype, txt, "Info", "dns")
                    count += 1
            except Exception:
                pass
        await manager.log(ws, f"[DNS] Found {count} DNS records.")


# ═══════════════════════════════════════════════════════════════════════════
# CRT.SH MODULE
# ═══════════════════════════════════════════════════════════════════════════

async def crtsh_module(target: str, ws: WebSocket):
    await manager.log(ws, "[CRT.SH] Querying certificate transparency logs...")
    url = f"https://crt.sh/?q=%25.{target}&output=json"
    data = None
    max_retries = 4

    for attempt in range(1, max_retries + 1):
        try:
            async with httpx.AsyncClient(timeout=15.0, verify=False) as client:
                resp = await client.get(
                    url,
                    headers={
                        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
                        'Accept': 'application/json',
                    }
                )
                if resp.status_code == 200:
                    content = resp.text
                    if content and content.strip():
                        try:
                            data = json.loads(content)
                            break
                        except json.JSONDecodeError:
                            await manager.log(ws, f"[WARN] crt.sh malformed JSON, retry {attempt}/{max_retries}...")
                            await asyncio.sleep(1.5 ** attempt)
                    else:
                        await manager.log(ws, f"[WARN] crt.sh empty response, retry {attempt}/{max_retries}...")
                        await asyncio.sleep(1.5 ** attempt)
                elif resp.status_code == 429:
                    wait = 3 ** attempt
                    await manager.log(ws, f"[WARN] crt.sh rate limited (429), waiting {wait}s...")
                    await asyncio.sleep(wait)
                else:
                    await manager.log(ws, f"[WARN] crt.sh HTTP {resp.status_code}, retry {attempt}/{max_retries}...")
                    await asyncio.sleep(1.5 ** attempt)
        except (httpx.TimeoutException, httpx.ConnectError):
            wait = 2 ** attempt
            await manager.log(ws, f"[WARN] crt.sh timeout, retry {attempt}/{max_retries} in {wait}s...")
            await asyncio.sleep(wait)
        except Exception as e:
            await manager.log(ws, f"[WARN] crt.sh error: {str(e)[:80]}, retry {attempt}/{max_retries}...")
            await asyncio.sleep(1.5 ** attempt)

    if data and isinstance(data, list):
        subs = set()
        for e in data:
            name = e.get('name_value', '').lower()
            if '*' not in name and (name.endswith(f".{target}") or name == target):
                for sub in name.split('\n'):
                    sub_clean = sub.strip()
                    if sub_clean:
                        subs.add(sub_clean)
        shown = 0
        for sub in sorted(subs)[:50]:
            await manager.result(ws, sub, "Passive (crt.sh)", "SSL certificate transparency log", "Info", "sub")
            shown += 1
        await manager.log(ws, f"[CRT.SH] SUCCESS: Found {len(subs)} unique subdomains (showing {shown})")
    else:
        # CertSpotter fallback
        await manager.log(ws, "[CRT.SH] crt.sh failed. Trying CertSpotter fallback...")
        try:
            fallback_url = (
                f"https://api.certspotter.com/v1/issuances?domain={target}"
                "&include_subdomains=true&expand=dns_names"
            )
            async with httpx.AsyncClient(timeout=10.0, verify=False) as client:
                resp = await client.get(fallback_url, headers={'User-Agent': 'ReconRadar-APOLLO/6.0'})
                if resp.status_code == 200:
                    fallback_data = resp.json()
                    if isinstance(fallback_data, list):
                        subs = set()
                        for cert in fallback_data:
                            for name in cert.get('dns_names', []):
                                n = name.lower().strip()
                                if n.endswith(f".{target}") or n == target:
                                    if '*' not in n:
                                        subs.add(n)
                        shown = 0
                        for sub in sorted(subs)[:50]:
                            await manager.result(ws, sub, "Passive (CertSpotter)", "SSL certificate log (alt source)", "Info", "sub")
                            shown += 1
                        await manager.log(ws, f"[CRT.SH] Fallback SUCCESS: Found {len(subs)} subdomains via CertSpotter")
                        return
        except Exception:
            pass
        await manager.log(ws, "[WARN] crt.sh + fallback both failed. Continuing without CT data.")


# ═══════════════════════════════════════════════════════════════════════════
# SUBDOMAIN BRUTE-FORCE
# ═══════════════════════════════════════════════════════════════════════════

async def subdomain_bruteforce(target: str, ws: WebSocket, modules: dict):
    if not DNS_AVAILABLE:
        return

    takeover_enabled = modules.get('takeover', True)

    # Primary source: wordlist.json (falls back to DEFAULT_WORDLIST)
    wordlist_set: Set[str] = set(await asyncio.to_thread(_load_wordlist) or DEFAULT_WORDLIST)

    # Secondary source: data/subdomains.txt
    try:
        def _read_subdomains_txt():
            p = DATA_DIR / "subdomains.txt"
            if not p.exists():
                return None
            lines = p.read_text(encoding="utf-8").splitlines()
            return [ln.strip() for ln in lines
                    if ln.strip() and not ln.strip().startswith('#')]

        extra_words = await asyncio.to_thread(_read_subdomains_txt)
        if extra_words is None:
            await manager.log(ws, "[SUBDOMAIN] No data/subdomains.txt found — using default wordlist only.")
        else:
            await manager.log(ws, f"[SUBDOMAIN] Loaded {len(extra_words)} extra words from data/subdomains.txt")
            wordlist_set.update(extra_words)
    except Exception as _e:
        await manager.log(ws, f"[SUBDOMAIN] Error reading data/subdomains.txt: {_e}")

    wordlist = list(wordlist_set)
    await manager.log(ws, f"[SUBDOMAIN] Loaded {len(wordlist)} words from wordlist")

    signatures = await asyncio.to_thread(_load_signatures)

    resolver = dns.resolver.Resolver()
    resolver.timeout  = 2.0
    resolver.lifetime = 2.0

    sem = asyncio.Semaphore(50)
    found_count    = 0
    takeover_count = 0

    async def check_subdomain(word):
        nonlocal found_count, takeover_count
        async with sem:
            sub = f"{word}.{target}"
            cache_key = f"{sub}:A"
            cached_ip = _cache_get(_dns_cache, cache_key, DNS_CACHE_TTL)

            if cached_ip is False:
                pass
            elif cached_ip:
                await manager.result(ws, sub, "Active Subdomain", cached_ip, "Info", "sub")
                await manager.result(ws, sub, "A Record", cached_ip, "Info", "dns")
                found_count += 1
                return
            else:
                try:
                    answers = resolver.resolve(sub, 'A')
                    for rdata in answers:
                        ip = rdata.address
                        _cache_set(_dns_cache, cache_key, ip)
                        await manager.result(ws, sub, "Active Subdomain", ip, "Info", "sub")
                        await manager.result(ws, sub, "A Record", ip, "Info", "dns")
                        found_count += 1
                        return
                except Exception:
                    _cache_set(_dns_cache, cache_key, False)

            if takeover_enabled:
                try:
                    cname_answers = resolver.resolve(sub, 'CNAME')
                    for rdata in cname_answers:
                        cname = rdata.target.to_text().rstrip('.')
                        cname_lower = cname.lower()
                        matched_sig = None
                        matched_service = ""
                        for sig, svc, _ in signatures:
                            if sig in cname_lower:
                                matched_sig = sig
                                matched_service = svc
                                break

                        if matched_sig:
                            is_vuln, reason, service = await verify_takeover(sub, cname)
                            if is_vuln:
                                takeover_count += 1
                                detail = f"CNAME: {cname} ({service}) | Verification: {reason}"
                                await manager.log(ws, f"[!!!] VERIFIED TAKEOVER: {sub} -> {cname} ({service})")
                                await manager.result(ws, sub, "VERIFIED TAKEOVER", detail, "High", "vuln")
                            else:
                                await manager.result(ws, sub, "CNAME (protected)", f"{cname} ({service}) - {reason}", "Medium", "sub")
                        else:
                            await manager.result(ws, sub, "CNAME", cname, "Info", "sub")
                except Exception:
                    pass

    tasks = [check_subdomain(w) for w in wordlist]
    await asyncio.gather(*tasks)
    await manager.log(ws, f"[SUBDOMAIN] Bruteforce complete: {found_count} active subdomains, "
                          f"{takeover_count} verified takeovers (scanned {len(wordlist)} words).")


# ═══════════════════════════════════════════════════════════════════════════
# HTTP PROBE MODULE
# ═══════════════════════════════════════════════════════════════════════════

async def httpx_probe(target: str, target_ip: str, open_ports: List[int], ws: WebSocket):
    if not HTTPX_AVAILABLE:
        await manager.log(ws, "[HTTPX] httpx not installed - skipping web probing")
        return

    await manager.log(ws, "[HTTPX] Probing web services (HTTP/HTTPS)...")

    web_ports = set(open_ports)
    common_ports = [80, 443, 8080, 8443, 3000, 5000, 8000, 8888, 9090, 9443,
                    9000, 4000, 7000, 10000, 9001, 9200, 5601, 1337, 3001, 5001, 7070, 7443]
    web_ports.update(common_ports)

    schemes     = ['https', 'http']
    tested      = set()
    probe_count = 0

    waf_patterns = {
        'cloudflare': 'Cloudflare', 'akamai': 'Akamai', 'incapsula': 'Incapsula',
        'imperva': 'Imperva', 'sucuri': 'Sucuri', 'modsecurity': 'ModSecurity',
        'stackpath': 'StackPath', 'fastly': 'Fastly', 'barracuda': 'Barracuda',
        'f5': 'F5 BIG-IP', 'aws': 'AWS WAF',
    }

    async def probe(port: int, scheme: str):
        nonlocal probe_count
        url = (f"{scheme}://{target}" if port in (80, 443)
               else f"{scheme}://{target}:{port}")
        if url in tested:
            return
        tested.add(url)
        try:
            async with httpx.AsyncClient(verify=False, timeout=7.0, follow_redirects=False) as client:
                resp = await client.get(url, headers={
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                                  'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
                    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                })
                server    = resp.headers.get('Server', '')
                x_powered = resp.headers.get('X-Powered-By', '')
                location  = resp.headers.get('Location', '')
                tech_parts = []
                if server:   tech_parts.append(server)
                if x_powered: tech_parts.append(x_powered)

                cf_ray = resp.headers.get('cf-ray', '')
                waf_detected = ""
                for pattern, name in waf_patterns.items():
                    if pattern in server.lower() or pattern in str(resp.headers).lower():
                        waf_detected = name
                        break
                if cf_ray and not waf_detected:
                    waf_detected = "Cloudflare"
                if 'x-sucuri-id' in resp.headers or 'x-sucuri-cache' in resp.headers:
                    waf_detected = "Sucuri"

                title = ""
                if resp.text:
                    m = re.search(r'<title[^>]*>(.*?)</title>', resp.text, re.IGNORECASE | re.DOTALL)
                    if m:
                        title = m.group(1).strip()[:80]

                details = f"HTTP {resp.status_code}"
                if title:      details += f" | Title: {title}"
                if tech_parts: details += f" | {' | '.join(tech_parts)}"
                if location:   details += f" | Redirect: {location[:80]}"

                await manager.log(ws, f"[HTTP] {url} -> {resp.status_code} [{server or 'no-server'}]")
                await manager.result(ws, url, waf_detected or server[:30] or "-", details,
                                     str(resp.status_code), "web")
                probe_count += 1
        except Exception:
            pass

    sem = asyncio.Semaphore(20)

    async def bounded_probe(port, scheme):
        async with sem:
            await probe(port, scheme)

    tasks = [
        bounded_probe(p, s) for p in web_ports for s in schemes
        if not (p == 443 and s == 'http') and not (p == 80 and s == 'https')
    ]
    await asyncio.gather(*tasks)
    await manager.log(ws, f"[HTTPX] Web probe complete. {probe_count} services responded.")


# ═══════════════════════════════════════════════════════════════════════════
# OSINT MODULE  (35+ sources)
# ═══════════════════════════════════════════════════════════════════════════

async def osint_module(target: str, ws: WebSocket):
    await manager.log(ws, "[OSINT] Gathering open-source intelligence links...")

    osint_links = [
        # ── Archive & History ──────────────────────────────────────────────
        ("Wayback Machine",     "Archive",          f"https://web.archive.org/web/*/{target}"),
        ("URLScan.io",          "Scan History",     f"https://urlscan.io/domain/{target}"),
        ("CommonCrawl",         "Web Crawl",        f"https://index.commoncrawl.org/CC-MAIN-2024-10-index?url=*.{target}&output=json"),

        # ── Search Engines (Dorks) ─────────────────────────────────────────
        ("Google Dork",         "Subdomains",       f"https://www.google.com/search?q=site%3A{target}"),
        ("Google Dork",         "Exposed Files",    f"https://www.google.com/search?q=site%3A{target}+ext%3Aphp+OR+ext%3Ajson+OR+ext%3Axml"),
        ("Bing Search",         "Domain Search",    f"https://www.bing.com/search?q=site%3A{target}"),

        # ── Threat Intelligence ────────────────────────────────────────────
        ("Shodan",              "Network Search",   f"https://www.shodan.io/search?query=hostname%3A{target}"),
        ("Censys",              "Host Search",      f"https://search.censys.io/search?resource=hosts&q={target}"),
        ("ZoomEye",             "Cyberspace",       f"https://www.zoomeye.org/searchResult?q={target}"),
        ("FOFA",                "Asset Discovery",  f"https://en.fofa.info/result?qbase64={target}"),
        ("Netlas",              "Network Intel",    f"https://app.netlas.io/domains/?q={target}"),
        ("FullHunt",            "Attack Surface",   f"https://fullhunt.io/domain/{target}"),
        ("LeakIX",              "Service Leaks",    f"https://leakix.net/domain/{target}"),
        ("Criminal IP",         "Threat Intel",     f"https://www.criminalip.io/domain/report?domain={target}"),
        ("BinaryEdge",          "Attack Surface",   f"https://www.binaryedge.io/domain/{target}"),
        ("GreyNoise",           "IP Noise",         f"https://viz.greynoise.io/query/?gnql={target}"),
        ("Onyphe",              "Threat Intel",     f"https://www.onyphe.io/search?q={target}"),
        ("Pulsedive",           "Threat Feed",      f"https://pulsedive.com/indicator/?ioc={target}"),
        ("AlienVault OTX",      "IOC Lookup",       f"https://otx.alienvault.com/indicator/domain/{target}"),

        # ── DNS & Passive DNS ──────────────────────────────────────────────
        ("SecurityTrails",      "DNS History",      f"https://securitytrails.com/domain/{target}/dns"),
        ("VirusTotal",          "Domain Report",    f"https://www.virustotal.com/gui/domain/{target}/details"),
        ("DNSDumpster",         "Subdomain Map",    f"https://dnsdumpster.com/domain/{target}"),
        ("Robtex",              "Passive DNS",      f"https://www.robtex.com/dns-lookup/{target}"),
        ("ViewDNS",             "DNS Tools",        f"https://viewdns.info/iphistory/?domain={target}"),
        ("MXToolbox",           "DNS Lookup",       f"https://mxtoolbox.com/SuperTool.aspx?action=a%3A{target}"),
        ("HackerTarget",        "DNS Recon",        f"https://hackertarget.com/find-dns-host-records/?q={target}"),
        ("RapidDNS",            "Subdomain Enum",   f"https://rapiddns.io/subdomain/{target}"),
        ("Chaos (PD)",          "Subdomain Data",   f"https://chaos.projectdiscovery.io/#/"),

        # ── Exposed Data & Leaks ───────────────────────────────────────────
        ("GrayHatWarfare",      "Open Buckets",     f"https://buckets.grayhatwarfare.com/results?search={target}"),
        ("Dehashed",            "Credential Leaks", f"https://dehashed.com/search?query={target}"),
        ("IntelX",              "Full Search",      f"https://intelx.io/?s={target}"),
        ("Grep.app",            "Code Search",      f"https://grep.app/search?q={target}"),
        ("GitHub Search",       "Code Exposure",    f"https://github.com/search?q={target}&type=code"),
        ("PublicWWW",           "Source Code",      f"https://publicwww.com/websites/{target}/"),

        # ── Technology Fingerprint ─────────────────────────────────────────
        ("BuiltWith",           "Tech Stack",       f"https://builtwith.com/{target}"),
        ("Wappalyzer",          "CMS/Tech",         f"https://www.wappalyzer.com/lookup/{target}"),
        ("WhatCMS",             "CMS Detect",       f"https://whatcms.org/?s={target}"),
    ]

    # Additional sources from data/osint.txt
    try:
        def _read_osint_txt():
            p = DATA_DIR / "osint.txt"
            if not p.exists():
                return None
            entries = []
            for ln in p.read_text(encoding="utf-8").splitlines():
                ln = ln.strip()
                if not ln or ln.startswith('#'):
                    continue
                parts = [x.strip() for x in ln.split('|')]
                if len(parts) >= 3:
                    entries.append((parts[0], parts[1], parts[2]))
            return entries

        custom_osint = await asyncio.to_thread(_read_osint_txt)
        if custom_osint is None:
            await manager.log(ws, "[OSINT] No data/osint.txt found — using built-in sources only.")
        else:
            await manager.log(ws, f"[OSINT] Loaded {len(custom_osint)} custom sources from data/osint.txt")
            for src, stype, url_tpl in custom_osint:
                osint_links.append((src, stype, url_tpl.replace('{target}', target)))
    except Exception as _e:
        await manager.log(ws, f"[OSINT] Error reading data/osint.txt: {_e}")

    for source, stype, link in osint_links:
        await manager.result(ws, source, stype, link, "Info", "osint")
    await manager.log(ws, f"[OSINT] Added {len(osint_links)} intelligence links.")


# ═══════════════════════════════════════════════════════════════════════════
# HTTP VULNERABILITY SCANNER
# ═══════════════════════════════════════════════════════════════════════════

async def http_vuln_scan(target: str, ws: WebSocket):
    if not HTTPX_AVAILABLE:
        return

    await manager.log(ws, "[VULN] Running HTTP vulnerability checks...")
    vuln_count = 0
    base_urls = [f"https://{target}", f"http://{target}"]

    SECURITY_HEADERS = {
        'Strict-Transport-Security':  ('Missing HSTS',            'High',   'Enables protocol downgrade / MITM attacks'),
        'Content-Security-Policy':    ('Missing CSP',             'Medium', 'No XSS content policy enforced'),
        'X-Frame-Options':            ('Missing X-Frame-Options', 'Medium', 'Site may be vulnerable to clickjacking'),
        'X-Content-Type-Options':     ('Missing X-Content-Type',  'Low',    'MIME-type sniffing not blocked'),
        'Referrer-Policy':            ('Missing Referrer-Policy', 'Low',    'Referrer data may leak to third parties'),
        'Permissions-Policy':         ('Missing Permissions-Policy','Low',  'Browser feature access not restricted'),
    }
    LEAK_HEADERS = {
        'Server':               'Server version disclosure',
        'X-Powered-By':         'Technology stack disclosure',
        'X-AspNet-Version':     'ASP.NET version disclosure',
        'X-AspNetMvc-Version':  'ASP.NET MVC version disclosure',
    }

    for base_url in base_urls:
        try:
            async with httpx.AsyncClient(verify=False, timeout=10.0, follow_redirects=True) as client:
                resp = await client.get(base_url, headers={'User-Agent': 'Mozilla/5.0 (ReconRadar-APOLLO/6.0)'})
                resp_headers_lower = {k.lower(): v for k, v in resp.headers.items()}

                for header, (threat, sev, detail) in SECURITY_HEADERS.items():
                    if header.lower() not in resp_headers_lower:
                        await manager.result(ws, base_url, threat, detail, sev, "vuln")
                        vuln_count += 1

                for header, threat in LEAK_HEADERS.items():
                    value = resp.headers.get(header, '')
                    if value:
                        detail = f"Header '{header}' exposes: {value[:120]}"
                        await manager.result(ws, base_url, threat, detail, "Low", "vuln")
                        vuln_count += 1

                if base_url.startswith('http://') and resp.status_code == 200:
                    await manager.result(ws, base_url, "HTTP without redirect",
                        "Site responds on HTTP 200 without redirecting to HTTPS", "Medium", "vuln")
                    vuln_count += 1
            break
        except Exception:
            continue

    SENSITIVE_PATHS = [
        ('/.env',                'Exposed .env file',        'High',   'Environment secrets/API keys may be exposed'),
        ('/.git/config',         'Exposed Git config',       'High',   'Git repository metadata exposed'),
        ('/.git/HEAD',           'Exposed Git HEAD',         'High',   'Git repository may be downloadable'),
        ('/wp-login.php',        'WordPress Login',          'Medium', 'WordPress admin login panel exposed'),
        ('/wp-admin/',           'WordPress Admin',          'Medium', 'WordPress admin area accessible'),
        ('/admin/',              'Admin Panel',              'Medium', 'Admin interface potentially exposed'),
        ('/phpmyadmin/',         'phpMyAdmin',               'High',   'Database admin UI publicly accessible'),
        ('/adminer.php',         'Adminer DB UI',            'High',   'Database management tool exposed'),
        ('/config.php',          'Config file',              'High',   'PHP config file may expose credentials'),
        ('/server-status',       'Apache server-status',     'Medium', 'Apache mod_status information disclosure'),
        ('/server-info',         'Apache server-info',       'Medium', 'Apache server configuration exposed'),
        ('/.htaccess',           'Exposed .htaccess',        'Medium', 'Apache config rules exposed'),
        ('/robots.txt',          'robots.txt',               'Low',    'May reveal hidden paths'),
        ('/sitemap.xml',         'Sitemap',                  'Low',    'Enumerates all public URLs'),
        ('/crossdomain.xml',     'crossdomain.xml',          'Low',    'Flash cross-domain policy'),
        ('/api/swagger.json',    'Swagger API Docs',         'Medium', 'API specification exposed publicly'),
        ('/swagger-ui.html',     'Swagger UI',               'Medium', 'API explorer publicly accessible'),
        ('/api/v1/',             'API v1 endpoint',          'Low',    'REST API endpoint enumerated'),
        ('/graphql',             'GraphQL endpoint',         'Medium', 'GraphQL may allow introspection'),
        ('/metrics',             'Prometheus metrics',       'High',   'Internal metrics/telemetry exposed'),
        ('/actuator',            'Spring Boot Actuator',     'High',   'Internal application management endpoint'),
        ('/actuator/env',        'Actuator /env',            'High',   'Spring Boot environment variables exposed'),
        ('/debug',               'Debug endpoint',           'High',   'Debug interface potentially accessible'),
        ('/console',             'Console endpoint',         'High',   'Admin console potentially accessible'),
        ('/trace',               'Trace endpoint',           'Medium', 'Request trace data accessible'),
        ('/.DS_Store',           'Exposed .DS_Store',        'Medium', 'macOS directory listing metadata exposed'),
        ('/backup.zip',          'Backup archive',           'High',   'Backup file publicly downloadable'),
        ('/.well-known/security.txt', 'Security.txt',       'Low',    'Security policy file (informational)'),
    ]

    CONTENT_VERIFY: Dict[str, List[str]] = {
        '/.env':             ['DB_', 'APP_', 'SECRET', 'PASSWORD', 'KEY=', 'TOKEN', 'DATABASE_URL'],
        '/.git/config':      ['[core]', '[remote', 'repositoryformatversion', 'filemode'],
        '/.git/HEAD':        ['ref: refs/', 'refs/heads/'],
        '/wp-login.php':     ['wp-login', 'WordPress', 'user_login', 'wp-submit'],
        '/wp-admin/':        ['wp-admin', 'WordPress', 'Dashboard'],
        '/phpmyadmin/':      ['phpMyAdmin', 'pma_', 'PMA_', 'phpmyadmin'],
        '/adminer.php':      ['adminer', 'Adminer', 'db=', 'username='],
        '/server-status':    ['Apache Server Status', 'Server Version', 'Current Time', 'Total Accesses'],
        '/server-info':      ['Apache Server Information', 'Server Built', 'Module Name'],
        '/.htaccess':        ['RewriteEngine', 'Options', 'AllowOverride', 'Deny', 'Allow', 'AuthType'],
        '/robots.txt':       ['User-agent:', 'Disallow:', 'Allow:'],
        '/sitemap.xml':      ['<urlset', '<sitemap', 'xmlns', '<url>'],
        '/crossdomain.xml':  ['cross-domain-policy', 'allow-access-from'],
        '/api/swagger.json': ['swagger', 'openapi', '"paths"', '"info"'],
        '/swagger-ui.html':  ['swagger-ui', 'SwaggerUI', 'swagger'],
        '/graphql':          ['__schema', 'query', 'mutation', 'GraphQL', 'graphql'],
        '/metrics':          ['# HELP', '# TYPE', 'go_', 'process_', 'http_requests'],
        '/actuator':         ['{"_links"', '"health"', '"info"', 'actuator'],
        '/actuator/env':     ['{"activeProfiles"', '"propertySources"', '"systemProperties"'],
        '/debug':            ['debug', 'Debug', 'stack', 'traceback', 'exception'],
        '/console':          ['console', 'Console', 'terminal', 'shell', 'H2 Console'],
        '/backup.zip':       [],
        '/.DS_Store':        [],
    }

    FALSE_POSITIVE_INDICATORS = [
        '404 not found', 'page not found', 'not found',
        '403 forbidden', 'access denied', 'forbidden',
        'error 404', 'error 403', 'error 400',
        'no such file', 'file not found', 'does not exist',
        'could not be found', "couldn't be found",
        '502 bad gateway', '503 service unavailable',
        'cloudflare', 'arvancloud', 'request blocked',
        "this site can't be reached",
    ]

    sem = asyncio.Semaphore(15)

    async def check_path(base_url: str, path: str, threat: str, sev: str, detail: str):
        nonlocal vuln_count
        async with sem:
            url = base_url.rstrip('/') + path
            try:
                async with httpx.AsyncClient(verify=False, timeout=6.0, follow_redirects=False) as client:
                    resp = await client.get(url, headers={'User-Agent': 'Mozilla/5.0 (ReconRadar-APOLLO/6.0)'})
                    if resp.status_code not in (200, 206, 401, 403):
                        return
                    body_bytes = resp.content
                    body_text  = body_bytes.decode('utf-8', errors='ignore')
                    body_lower = body_text.lower()
                    if len(body_bytes) < 20:
                        return
                    if resp.status_code in (200, 206):
                        if any(fp in body_lower for fp in FALSE_POSITIVE_INDICATORS):
                            return
                        for path_key, sigs in CONTENT_VERIFY.items():
                            if path.startswith(path_key) and sigs:
                                if not any(sig in body_text for sig in sigs):
                                    return
                        if len(body_bytes) < 100:
                            ct = resp.headers.get('Content-Type', '').lower()
                            if 'html' in ct and path not in ('/robots.txt', '/.git/HEAD'):
                                return
                    status_note   = f"HTTP {resp.status_code}"
                    full_detail   = f"{detail} [{status_note}] → {url}"
                    effective_sev = sev if resp.status_code == 200 else "Low"
                    if resp.status_code in (200, 206):
                        await manager.log(ws, f"[VULN] {threat} found: {url} [{resp.status_code}]")
                    await manager.result(ws, url, threat, full_detail, effective_sev, "vuln")
                    vuln_count += 1
            except Exception:
                pass

    tasks = [check_path(f"https://{target}", path, threat, sev, detail)
             for path, threat, sev, detail in SENSITIVE_PATHS]
    await asyncio.gather(*tasks)

    # Additional paths from data/paths.txt
    try:
        def _read_paths_txt():
            p = DATA_DIR / "paths.txt"
            if not p.exists():
                return None
            lines = p.read_text(encoding="utf-8").splitlines()
            return [ln.strip() for ln in lines
                    if ln.strip() and ln.strip().startswith('/')
                    and not ln.strip().startswith('#')]

        custom_paths = await asyncio.to_thread(_read_paths_txt)
        if custom_paths is None:
            await manager.log(ws, "[VULN] No data/paths.txt found — skipping custom paths.")
        else:
            await manager.log(ws, f"[VULN] Loaded {len(custom_paths)} custom paths from data/paths.txt")
            custom_tasks = [
                check_path(
                    f"https://{target}",
                    path,
                    f"Custom Path: {path}",
                    "Medium",
                    "Found via custom paths list",
                )
                for path in custom_paths
            ]
            await asyncio.gather(*custom_tasks)
    except Exception as _e:
        await manager.log(ws, f"[VULN] Error reading data/paths.txt: {_e}")

    await manager.log(ws, f"[VULN] HTTP vulnerability scan complete. {vuln_count} findings.")


# ═══════════════════════════════════════════════════════════════════════════
# MAIN RECON ORCHESTRATOR
# ═══════════════════════════════════════════════════════════════════════════

async def perform_recon(target: str, nmap_args: str, ws: WebSocket,
                        modules: dict, scan_id: str):
    start_time = datetime.utcnow().isoformat()
    try:
        manager.start_scan_buffer(ws, scan_id)
        await asyncio.to_thread(
            _index_upsert, scan_id, target, start_time, "running"
        )

        # Resolve target
        await manager.log(ws, f"[RESOLVE] Resolving {target}...")
        target_ip = None
        try:
            target_ip = socket.gethostbyname(target)
            await manager.log(ws, f"[+] {target} -> {target_ip}")
            await manager.result(ws, target, "A Record", target_ip, "Info", "dns")
        except socket.gaierror:
            try:
                socket.inet_aton(target)
                target_ip = target
                await manager.log(ws, f"[+] Target is IP: {target_ip}")
            except socket.error:
                await manager.log(ws, f"[FATAL] Cannot resolve {target}")
                await manager.status(ws, "error")
                await asyncio.to_thread(_index_upsert, scan_id, target, start_time,
                                        "error", datetime.utcnow().isoformat())
                return

        # Phase 1: DNS + WHOIS
        await manager.log(ws, "[PHASE 1/7] DNS Enumeration + WHOIS")
        await dns_whois_module(target, ws, modules)

        # Phase 2: CRT.SH
        if modules.get('subdomain', True):
            await manager.log(ws, "[PHASE 2/7] Certificate Transparency Logs (crt.sh)")
            await crtsh_module(target, ws)

        # Phase 3: DNS Zone Transfer
        if modules.get('dnszone', True):
            await manager.log(ws, "[PHASE 3/7] DNS Zone Transfer Check")
            await dns_zone_transfer(target, ws)

        # Phase 4: OSINT
        if modules.get('osint', True):
            await manager.log(ws, "[PHASE 4/7] Open Source Intelligence (35+ sources)")
            await osint_module(target, ws)

        # Phase 5: Nmap / socket scan
        await manager.log(ws, "[PHASE 5/7] Nmap Port Scan")
        effective_nmap_args = nmap_args
        if '-Pn' not in effective_nmap_args and '-sn' not in effective_nmap_args:
            effective_nmap_args = effective_nmap_args.strip() + ' -Pn'
        await manager.log(ws, f"[NMAP] Starting scan: {effective_nmap_args}")

        open_ports = []
        ports_data = []

        if NMAP_AVAILABLE:
            try:
                ports_data, nmap_warning = await asyncio.to_thread(
                    run_nmap_scan, target_ip, effective_nmap_args
                )
                if nmap_warning:
                    await manager.log(ws, nmap_warning)
            except Exception as e:
                await manager.log(ws, f"[NMAP ERROR] {str(e)[:200]}")

        if not ports_data:
            await manager.log(ws, "[NMAP] 0 results from nmap. Running socket fallback scanner...")
            try:
                socket_results = await asyncio.to_thread(
                    socket_port_scan, target_ip, COMMON_PORTS, 1.2
                )
                if socket_results:
                    await manager.log(ws, f"[SOCKET] Fallback found {len(socket_results)} open ports")
                    ports_data = socket_results
                else:
                    await manager.log(ws, "[SOCKET] Fallback found 0 open ports — host may be behind CDN/firewall")
            except Exception as e:
                await manager.log(ws, f"[SOCKET] Fallback error: {str(e)[:100]}")

        critical_ports = {22, 23, 3389, 1433, 3306, 5900, 5800, 6379, 27017,
                          11211, 9200, 5432, 1521, 445, 135, 139, 389, 636,
                          25, 110, 143, 993, 995, 2375, 2376, 50070}
        for p in ports_data:
            p_info    = f"{p['host']}:{p['port']}/{p['protocol']}"
            state_str = p['state'].upper()
            svc_out   = p['service'][:100]
            sev = ("High"   if p['state'] == 'open' and p['port'] in critical_ports else
                   "Medium" if p['state'] == 'open' else "Info")
            if p['state'] == 'open':
                await manager.log(ws, f"[PORT] {p_info} | {p['state']} | {svc_out[:60]}")
            await manager.result(ws, p_info, state_str, svc_out, sev, "port")
            if p['state'] == 'open':
                open_ports.append(p['port'])
            for script_name, script_out in p.get('scripts', {}).items():
                script_text = str(script_out)
                is_vuln     = 'VULNERABLE' in script_text.upper() or 'EXPLOIT' in script_text.upper()
                script_sev  = "High" if is_vuln else "Medium"
                vuln_kws    = ('vuln', 'exploit', 'brute', 'cve', 'backdoor', 'malware',
                               'auth-bypass', 'injection', 'overflow', 'dos', 'rce')
                if any(kw in script_name.lower() for kw in vuln_kws) or is_vuln:
                    detail = script_text[:300].replace('\n', ' | ')
                    await manager.result(ws, p_info, script_name, detail, script_sev, "vuln")
                    if is_vuln:
                        await manager.log(ws, f"[VULN] {p_info} → {script_name}: VULNERABLE")

        open_count = len([p for p in ports_data if p['state'] == 'open'])
        await manager.log(ws, f"[NMAP] Found {open_count} open ports.")

        # Phase 6: Subdomain brute-force + takeover
        if modules.get('subdomain', True):
            await manager.log(ws, "[PHASE 6/7] Subdomain Bruteforce + Takeover Detection")
            await subdomain_bruteforce(target, ws, modules)

        # Phase 7: HTTP probe
        if modules.get('web', True):
            await manager.log(ws, "[PHASE 7/7] HTTP Service Probing")
            await httpx_probe(target, target_ip, open_ports, ws)

        # Phase 7b: HTTP vuln scan
        if modules.get('web', True):
            await manager.log(ws, "[PHASE 7b] HTTP Vulnerability Checks")
            await http_vuln_scan(target, ws)

        # Save HTML report
        end_ts = datetime.utcnow().isoformat()
        scan_results = manager.get_scan_buffer(scan_id)
        if scan_results:
            await asyncio.to_thread(
                _save_html_report, scan_id, target, start_time, scan_results
            )
        await asyncio.to_thread(
            _index_upsert, scan_id, target, start_time, "done", end_ts
        )
        manager.clear_scan_buffer(scan_id)

        await asyncio.sleep(0.3)
        await manager.log(ws, f"[+] APOLLO scan COMPLETE. HTML report saved to reports/{scan_id}.html")
        await manager.log(ws, f"[+] GitHub: https://github.com/Nexvir | ReconRadar v6.0 APOLLO")
        await manager.status(ws, "done")

    except asyncio.CancelledError:
        await asyncio.to_thread(
            _index_upsert, scan_id, target, start_time,
            "stopped", datetime.utcnow().isoformat()
        )
        manager.clear_scan_buffer(scan_id)
        await manager.log(ws, "[SYSTEM] Scan cancelled by user.")
        await manager.status(ws, "stopped")
        raise
    except Exception as e:
        import traceback
        tb = traceback.format_exc()
        await asyncio.to_thread(
            _index_upsert, scan_id, target, start_time,
            "error", datetime.utcnow().isoformat()
        )
        manager.clear_scan_buffer(scan_id)
        await manager.log(ws, f"[FATAL] {type(e).__name__}: {e}")
        await manager.log(ws, f"[DEBUG] {tb[-300:]}")
        await manager.status(ws, "error")


# ═══════════════════════════════════════════════════════════════════════════
# REST / WEBSOCKET ENDPOINTS
# ═══════════════════════════════════════════════════════════════════════════

@app.get("/", response_class=HTMLResponse)
async def dashboard():
    return HTMLResponse(content=HTML_TEMPLATE, status_code=200)


@app.websocket("/ws")
async def ws_endpoint(ws: WebSocket):
    await manager.connect(ws)
    current_task    = None
    current_scan_id = None
    try:
        while True:
            raw = await ws.receive_text()
            try:
                payload = json.loads(raw)
                if payload.get("action") == "start_scan":
                    target    = payload.get("target", "").strip()
                    nmap_args = payload.get("nmap_args", "-sV -T4 -F -n")
                    modules   = payload.get("modules", {
                        "dns": True, "whois": True, "subdomain": True,
                        "takeover": True, "web": True, "dnszone": True, "osint": True,
                    })
                    scan_id = payload.get("scan_id", str(time.time()))
                    if target:
                        current_scan_id = scan_id
                        current_task = asyncio.create_task(
                            perform_recon(target, nmap_args, ws, modules, scan_id)
                        )
                        manager.scan_tasks[scan_id] = current_task
                elif payload.get("action") == "stop_scan":
                    sid = payload.get("scan_id")
                    if sid and sid in manager.scan_tasks:
                        manager.scan_tasks[sid].cancel()
                        del manager.scan_tasks[sid]
                        await manager.log(ws, "[SYSTEM] Stop command received. Terminating scan...")
            except json.JSONDecodeError:
                pass
    except WebSocketDisconnect:
        if current_task and not current_task.done():
            current_task.cancel()
        manager.disconnect(ws)


@app.get("/history")
async def get_history():
    """Return list of all past scans from index."""
    def _query():
        try:
            return json.loads(INDEX_FILE.read_text(encoding="utf-8"))
        except Exception:
            return []

    data = await asyncio.to_thread(_query)
    return JSONResponse(content=data)


@app.get("/history/{scan_id}", response_class=HTMLResponse)
async def get_scan_report(scan_id: str):
    """Return the saved HTML report for a specific scan."""
    report_path = REPORTS_DIR / f"{scan_id}.html"
    if not report_path.exists():
        raise HTTPException(status_code=404, detail=f"Report for scan '{scan_id}' not found")
    return HTMLResponse(content=report_path.read_text(encoding="utf-8"), status_code=200)


# ═══════════════════════════════════════════════════════════════════════════
# STARTUP + ENTRYPOINT
# ═══════════════════════════════════════════════════════════════════════════

@app.on_event("startup")
async def startup_event():
    await asyncio.to_thread(init_storage)
    logger.info("ReconRadar APOLLO v6.0 started — storage initialised in data/ and reports/")


if __name__ == "__main__":
    init_storage()
    print("""
╔═══════════════════════════════════════════════════════════════════════════╗
║         ReconRadar APOLLO v6.0 - Ultimate Reconnaissance Framework       ║
║                          github.com/Nexvir                                ║
║     Running on http://127.0.0.1:8000                                     ║
║                                                                           ║
║  ✨ What's New in v6.0:                                                   ║
║  ✅ SQLite removed — each scan saved as standalone HTML report            ║
║  ✅ reports/{scan_id}.html — fully styled HTML per scan                   ║
║  ✅ data/wordlist.json  — editable brute-force wordlist                   ║
║  ✅ data/signatures.json — editable takeover signatures                   ║
║  ✅ GET /history  — list all past scans (from reports/index.json)         ║
║  ✅ GET /history/{scan_id} — open full HTML report in browser             ║
║  ✅ OSINT expanded to 35+ sources (Shodan, Netlas, FullHunt,              ║
║     LeakIX, Criminal IP, GreyNoise, OTX, Pulsedive, GitHub, ...)         ║
║  ✅ DNS cache (5 min TTL) + WHOIS cache (24 h TTL)                        ║
║  ✅ RotatingFileHandler logging → reconradar.log                          ║
║  ✅ No dependencies on SQLite — zero DB setup required                    ║
║                                                                           ║
║  🛡️  For authorized security testing only                                 ║
╚═══════════════════════════════════════════════════════════════════════════╝
    """)
    uvicorn.run(app, host="127.0.0.1", port=8000, log_level="info")
