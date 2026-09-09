"""
ReconRadar APOLLO v7.0 - Database Layer
-----------------------------------------
PostgreSQL/SQLite support with SQLAlchemy ORM
Optimized for high-performance reconnaissance operations
"""

import os
from datetime import datetime
from typing import Optional, List, Dict, Any
from pathlib import Path

from sqlalchemy import (
    create_engine, Column, Integer, String, Text, DateTime, Boolean, 
    Float, ForeignKey, Index, JSON, event, func
)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship, Session
from sqlalchemy.pool import StaticPool

# ── Configuration ────────────────────────────────────────────────────────────

DATABASE_URL = os.getenv(
    "RECONRADAR_DB", 
    "sqlite:///reconradar.db?check_same_thread=False"
)

# Use PostgreSQL if available (better for production)
if DATABASE_URL.startswith("postgresql"):
    engine = create_engine(
        DATABASE_URL,
        pool_size=20,
        max_overflow=40,
        pool_pre_ping=True,
        pool_recycle=3600,
    )
else:
    # SQLite for standalone use
    engine = create_engine(
        DATABASE_URL.replace("?check_same_thread=False", ""),
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )

SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)
Base = declarative_base()


# ═══════════════════════════════════════════════════════════════════════════
# MODELS
# ═══════════════════════════════════════════════════════════════════════════

class Scan(Base):
    """Main scan session table"""
    __tablename__ = "scans"
    
    id = Column(String(64), primary_key=True)
    target = Column(String(512), nullable=False, index=True)
    target_ip = Column(String(64))
    status = Column(String(32), default="running", index=True)  # running, done, error, stopped
    started_at = Column(DateTime, default=datetime.utcnow, index=True)
    completed_at = Column(DateTime)
    duration_seconds = Column(Float)
    
    # Scan configuration
    nmap_args = Column(String(512))
    modules_enabled = Column(JSON)  # {"dns": true, "whois": true, ...}
    
    # Summary statistics
    total_findings = Column(Integer, default=0)
    subdomains_found = Column(Integer, default=0)
    open_ports_found = Column(Integer, default=0)
    vulnerabilities_found = Column(Integer, default=0)
    takeover_candidates = Column(Integer, default=0)
    
    # Relationships
    findings = relationship("Finding", back_populates="scan", cascade="all, delete-orphan")
    screenshots = relationship("Screenshot", back_populates="scan", cascade="all, delete-orphan")
    
    __table_args__ = (
        Index('idx_scan_status_target', 'status', 'target'),
    )


class Finding(Base):
    """Individual finding/result from scan"""
    __tablename__ = "findings"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    scan_id = Column(String(64), ForeignKey('scans.id', ondelete='CASCADE'), nullable=False, index=True)
    
    # Finding data
    category = Column(String(64), index=True)  # dns, sub, port, web, vuln, osint, takeover
    severity = Column(String(32), index=True)  # Info, Low, Medium, High, Critical
    
    # Dynamic columns stored as JSON for flexibility
    data = Column(JSON, nullable=False)  # {col1, col2, col3, extra...}
    
    # Denormalized fields for fast queries
    col1 = Column(String(512), index=True)
    col2 = Column(String(512))
    col3 = Column(Text)
    
    created_at = Column(DateTime, default=datetime.utcnow, index=True)
    
    # Relationships
    scan = relationship("Scan", back_populates="findings")
    
    __table_args__ = (
        Index('idx_finding_category_severity', 'category', 'severity'),
        Index('idx_finding_col1', 'col1'),
    )


class Screenshot(Base):
    """Website screenshots captured during scan"""
    __tablename__ = "screenshots"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    scan_id = Column(String(64), ForeignKey('scans.id', ondelete='CASCADE'), nullable=False, index=True)
    url = Column(String(1024), nullable=False)
    file_path = Column(String(512), nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow)
    status_code = Column(Integer)
    tech_stack = Column(JSON)  # Detected technologies
    
    # Relationships
    scan = relationship("Scan", back_populates="screenshots")


class Target(Base):
    """Tracked targets for monitoring changes over time"""
    __tablename__ = "targets"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    domain = Column(String(512), unique=True, nullable=False, index=True)
    first_seen = Column(DateTime, default=datetime.utcnow)
    last_scanned = Column(DateTime)
    scan_count = Column(Integer, default=0)
    
    # Cached data
    ip_addresses = Column(JSON)  # List of resolved IPs
    asn_info = Column(JSON)  # ASN, organization, country
    whois_cache = Column(JSON)
    
    # Monitoring
    monitor_enabled = Column(Boolean, default=False)
    monitor_interval_hours = Column(Integer, default=24)
    webhook_url = Column(String(1024))  # For notifications
    
    # Relationships (no direct FK - scans reference target by name)
    # Using viewonly=True since there's no FK column in scans table


class APIKey(Base):
    """API keys for authentication"""
    __tablename__ = "api_keys"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    key_hash = Column(String(128), unique=True, nullable=False, index=True)
    name = Column(String(256))
    created_at = Column(DateTime, default=datetime.utcnow)
    expires_at = Column(DateTime)
    is_active = Column(Boolean, default=True)
    
    # Rate limiting
    requests_today = Column(Integer, default=0)
    last_request = Column(DateTime)
    rate_limit_per_hour = Column(Integer, default=100)


class Cache(Base):
    """General purpose cache table"""
    __tablename__ = "cache"
    
    key = Column(String(512), primary_key=True)
    value = Column(JSON, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    expires_at = Column(DateTime, index=True)
    cache_type = Column(String(64), index=True)  # dns, whois, nmap, etc.


# ═══════════════════════════════════════════════════════════════════════════
# DATABASE OPERATIONS
# ═══════════════════════════════════════════════════════════════════════════

def init_db():
    """Create all tables"""
    Base.metadata.create_all(bind=engine)


def get_session() -> Session:
    """Get database session"""
    return SessionLocal()


def create_scan(
    scan_id: str,
    target: str,
    nmap_args: str = "",
    modules_enabled: Dict = None
) -> Scan:
    """Create a new scan record"""
    db = get_session()
    try:
        scan = Scan(
            id=scan_id,
            target=target,
            nmap_args=nmap_args,
            modules_enabled=modules_enabled or {},
            status="running"
        )
        db.add(scan)
        db.commit()
        db.refresh(scan)
        return scan
    finally:
        db.close()


def update_scan_status(
    scan_id: str,
    status: str,
    completed_at: datetime = None,
    **kwargs
) -> Optional[Scan]:
    """Update scan status and metadata"""
    db = get_session()
    try:
        scan = db.query(Scan).filter(Scan.id == scan_id).first()
        if not scan:
            return None
        
        scan.status = status
        if completed_at:
            scan.completed_at = completed_at
            if scan.started_at:
                scan.duration_seconds = (completed_at - scan.started_at).total_seconds()
        
        for key, value in kwargs.items():
            if hasattr(scan, key):
                setattr(scan, key, value)
        
        db.commit()
        db.refresh(scan)
        return scan
    finally:
        db.close()


def add_finding(
    scan_id: str,
    category: str,
    severity: str,
    data: Dict,
    col1: str = "",
    col2: str = "",
    col3: str = ""
) -> Finding:
    """Add a finding to a scan"""
    db = get_session()
    try:
        finding = Finding(
            scan_id=scan_id,
            category=category,
            severity=severity,
            data=data,
            col1=col1,
            col2=col2,
            col3=col3
        )
        db.add(finding)
        
        # Update scan statistics
        scan = db.query(Scan).filter(Scan.id == scan_id).first()
        if scan:
            scan.total_findings += 1
            if category == "sub":
                scan.subdomains_found += 1
            elif category == "port":
                scan.open_ports_found += 1
            elif category == "vuln":
                scan.vulnerabilities_found += 1
            elif category == "takeover":
                scan.takeover_candidates += 1
        
        db.commit()
        db.refresh(finding)
        return finding
    finally:
        db.close()


def add_finding_batch(
    scan_id: str,
    findings: List[Dict]
) -> int:
    """Add multiple findings in a batch (optimized)"""
    db = get_session()
    try:
        batch_objects = []
        for f in findings:
            batch_objects.append(Finding(
                scan_id=scan_id,
                category=f.get("category", "dns"),
                severity=f.get("severity", "Info"),
                data=f.get("data", {}),
                col1=f.get("col1", ""),
                col2=f.get("col2", ""),
                col3=f.get("col3", "")
            ))
        
        if batch_objects:
            db.bulk_save_objects(batch_objects)
            
            # Update scan total
            scan = db.query(Scan).filter(Scan.id == scan_id).first()
            if scan:
                scan.total_findings += len(batch_objects)
            
            db.commit()
        
        return len(batch_objects)
    finally:
        db.close()


def get_scan(scan_id: str) -> Optional[Scan]:
    """Get scan by ID"""
    db = get_session()
    try:
        return db.query(Scan).filter(Scan.id == scan_id).first()
    finally:
        db.close()


def get_scan_findings(scan_id: str, category: str = None) -> List[Finding]:
    """Get all findings for a scan, optionally filtered by category"""
    db = get_session()
    try:
        query = db.query(Finding).filter(Finding.scan_id == scan_id)
        if category:
            query = query.filter(Finding.category == category)
        return query.order_by(Finding.created_at).all()
    finally:
        db.close()


def get_scan_history(limit: int = 100, offset: int = 0) -> List[Scan]:
    """Get scan history"""
    db = get_session()
    try:
        return db.query(Scan)\
            .order_by(Scan.started_at.desc())\
            .offset(offset)\
            .limit(limit)\
            .all()
    finally:
        db.close()


def get_or_create_target(domain: str) -> Target:
    """Get existing target or create new one"""
    db = get_session()
    try:
        target = db.query(Target).filter(Target.domain == domain).first()
        if not target:
            target = Target(domain=domain)
            db.add(target)
            db.commit()
            db.refresh(target)
        return target
    finally:
        db.close()


def update_target_last_scanned(domain: str):
    """Update target's last scanned timestamp"""
    db = get_session()
    try:
        target = db.query(Target).filter(Target.domain == domain).first()
        if target:
            target.last_scanned = datetime.utcnow()
            target.scan_count += 1
            db.commit()
    finally:
        db.close()


def cache_set(key: str, value: Any, cache_type: str = "general", ttl_seconds: int = 3600):
    """Set cache entry"""
    db = get_session()
    try:
        from datetime import timedelta
        cache_entry = Cache(
            key=key,
            value=value,
            cache_type=cache_type,
            expires_at=datetime.utcnow() + timedelta(seconds=ttl_seconds)
        )
        db.merge(cache_entry)
        db.commit()
    finally:
        db.close()


def cache_get(key: str) -> Optional[Any]:
    """Get cache entry if not expired"""
    db = get_session()
    try:
        entry = db.query(Cache).filter(
            Cache.key == key,
            Cache.expires_at > datetime.utcnow()
        ).first()
        return entry.value if entry else None
    finally:
        db.close()


def cache_cleanup():
    """Remove expired cache entries"""
    db = get_session()
    try:
        db.query(Cache).filter(Cache.expires_at < datetime.utcnow()).delete()
        db.commit()
    finally:
        db.close()


def get_statistics() -> Dict:
    """Get overall system statistics"""
    db = get_session()
    try:
        total_scans = db.query(Scan).count()
        completed_scans = db.query(Scan).filter(Scan.status == "done").count()
        total_findings = db.query(Finding).count()
        total_targets = db.query(Target).count()
        
        # Severity breakdown
        severity_counts = db.query(
            Finding.severity, 
            func.count(Finding.id)
        ).group_by(Finding.severity).all()
        
        # Category breakdown
        category_counts = db.query(
            Finding.category,
            func.count(Finding.id)
        ).group_by(Finding.category).all()
        
        return {
            "total_scans": total_scans,
            "completed_scans": completed_scans,
            "total_findings": total_findings,
            "total_targets": total_targets,
            "severity_breakdown": dict(severity_counts),
            "category_breakdown": dict(category_counts)
        }
    finally:
        db.close()


# Event listener for connection setup (SQLite specific)
@event.listens_for(engine, "connect")
def set_sqlite_pragma(dbapi_connection, connection_record):
    """Optimize SQLite performance"""
    if 'sqlite' in DATABASE_URL:
        cursor = dbapi_connection.cursor()
        cursor.execute("PRAGMA journal_mode=WAL")
        cursor.execute("PRAGMA synchronous=NORMAL")
        cursor.execute("PRAGMA cache_size=10000")
        cursor.execute("PRAGMA temp_store=MEMORY")
        cursor.close()
