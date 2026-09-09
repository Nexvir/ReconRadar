"""
ReconRadar APOLLO v7.0 - Hash Cracker Module
----------------------------------------------
Advanced password hash cracking capabilities for ethical hacking
Supports multiple hash types with dictionary and rule-based attacks
Integrated with database for persistent storage of cracked passwords
"""

import hashlib
import hmac
import base64
import re
import os
import json
import time
import logging
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Tuple, Set
from collections import defaultdict

from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey, Index, JSON
from sqlalchemy.orm import relationship

from database import Base, get_session, engine

# ── Logging setup ────────────────────────────────────────────────────────────
logger = logging.getLogger("ReconRadar.HashCracker")

# ═══════════════════════════════════════════════════════════════════════════
# DATABASE MODEL FOR CRACKED HASHES
# ═══════════════════════════════════════════════════════════════════════════

class CrackedHash(Base):
    """Storage for cracked hashes"""
    __tablename__ = "cracked_hashes"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    hash_value = Column(String(256), nullable=False, index=True)
    hash_type = Column(String(64), nullable=False, index=True)  # md5, sha1, sha256, bcrypt, etc.
    plaintext = Column(String(1024), nullable=False)
    crack_time = Column(DateTime, default=datetime.utcnow)
    method = Column(String(64))  # dictionary, brute_force, rule_based, rainbow
    wordlist_used = Column(String(512))
    scan_id = Column(String(64), ForeignKey('scans.id'))
    
    # Metadata
    username = Column(String(256))  # Associated username if available
    source = Column(String(512))  # Where the hash was found
    
    __table_args__ = (
        Index('idx_hash_value_type', 'hash_value', 'hash_type'),
        Index('idx_crack_time', 'crack_time'),
    )


# ═══════════════════════════════════════════════════════════════════════════
# HASH TYPE DETECTION
# ═══════════════════════════════════════════════════════════════════════════

HASH_PATTERNS = {
    'MD5': {
        'pattern': r'^[a-fA-F0-9]{32}$',
        'length': 32,
        'example': '5f4dcc3b5aa765d61d8327deb882cf99',
        'description': 'MD5 - Fast, vulnerable to collision attacks'
    },
    'SHA1': {
        'pattern': r'^[a-fA-F0-9]{40}$',
        'length': 40,
        'example': '7c4a8d09ca3762af61e59520943dc26494f8941b',
        'description': 'SHA-1 - Deprecated, collision vulnerabilities known'
    },
    'SHA256': {
        'pattern': r'^[a-fA-F0-9]{64}$',
        'length': 64,
        'example': '5e884898da28047151d0e56f8dc6292773603d0d6aabbdd62a11ef721d1542d8',
        'description': 'SHA-256 - Secure, widely used'
    },
    'SHA384': {
        'pattern': r'^[a-fA-F0-9]{96}$',
        'length': 96,
        'example': '38b060a751ac96384cd9327eb1b1e36a21fdb71114be07434c0cc7bf63f6e1da274edebfe76f65fbd51ad2f14898b95b',
        'description': 'SHA-384 - Extended security'
    },
    'SHA512': {
        'pattern': r'^[a-fA-F0-9]{128}$',
        'length': 128,
        'example': 'b109f3bbbc244eb82441917ed06d618b9008dd09b3befd1b5e07394c706a8bb980b1d7785e5976ec049b46df5f1326af5a2ea6d103fd07c95385ffab0cacbc86',
        'description': 'SHA-512 - Maximum security in SHA-2 family'
    },
    'NTLM': {
        'pattern': r'^[a-fA-F0-9]{32}$',
        'length': 32,
        'example': '8846f7eaee8fb117ad06bdd830b7586c',
        'description': 'NTLM - Windows password hash'
    },
    'bcrypt': {
        'pattern': r'^\$2[aby]?\$\d+\$[./A-Za-z0-9]{53}$',
        'length': 60,
        'example': '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/X4.G0fZ.z6z6z6z6.',
        'description': 'bcrypt - Slow, secure, uses salt'
    },
    'argon2': {
        'pattern': r'^\$argon2\w?\$v=\d+\$m=\d+,t=\d+,p=\d+\$[.+A-Za-z0-9]+\$[.+A-Za-z0-9]+$',
        'example': '$argon2id$v=19$m=65536,t=3,p=4$c29tZXNhbHQ$RdescudvJCsgt3ub+b+dWRWJTmaaJObG',
        'description': 'Argon2 - Password hashing competition winner'
    },
    'PBKDF2': {
        'pattern': r'^pbkdf2:\d+:[a-fA-F0-9]+\$[a-fA-F0-9]+$',
        'example': 'pbkdf2:10000:53616c7465645f5f39393939$3b1f7e8e0e0e0e0e0e0e0e0e0e0e0e0e0e0e0e0e',
        'description': 'PBKDF2 - Key derivation function'
    },
    'MySQL': {
        'pattern': r'^\*[a-fA-F0-9]{40}$',
        'length': 41,
        'example': '*2470C0C06DEEE42C9FBD252695031C95B2367C78',
        'description': 'MySQL 4.1+ password hash'
    },
    'Django': {
        'pattern': r'^\w+\$\d+\$[a-zA-Z0-9]{12}\$[a-zA-Z0-9]{64}$',
        'example': 'pbkdf2_sha256$36000$ saltsalt$saltsaltsaltsaltsaltsaltsaltsaltsaltsaltsalt',
        'description': 'Django password hash'
    },
    'Base64': {
        'pattern': r'^[A-Za-z0-9+/]+=*$',
        'example': 'cGFzc3dvcmQ=',
        'description': 'Base64 encoded (not a hash, but often encountered)'
    }
}


def detect_hash_type(hash_string: str) -> Optional[str]:
    """Detect the type of hash based on pattern matching"""
    hash_string = hash_string.strip()
    
    # Check each hash type pattern
    for hash_type, info in HASH_PATTERNS.items():
        if re.match(info['pattern'], hash_string):
            return hash_type
    
    return None


# ═══════════════════════════════════════════════════════════════════════════
# WORDLIST MANAGEMENT
# ═══════════════════════════════════════════════════════════════════════════

DEFAULT_WORDLIST = [
    'password', '123456', '12345678', 'qwerty', 'abc123', 'monkey', 'master',
    'dragon', 'letmein', 'login', 'princess', 'admin', 'welcome', 'solo',
    'passw0rd', 'shadow', 'sunshine', 'iloveyou', 'fuckme', 'baseball',
    'football', 'password1', 'password123', 'changeme', '1234567', '123456789',
    '1234567890', 'batman', 'trustno1', 'superman', 'michael', 'ashley',
    'bailey', 'access', 'test', 'guest', 'root', 'administrator',
    'company', 'corporate', 'secret', 'private', 'public',
    'summer', 'winter', 'spring', 'autumn', 'fall',
    'january', 'february', 'march', 'april', 'may', 'june',
    'july', 'august', 'september', 'october', 'november', 'december',
    'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday',
    'P@ssw0rd', 'Password1', 'Welcome1', 'ChangeMe123', 'Admin123',
    'qwerty123', 'pass123', 'test123', 'demo123',
    'oracle', 'mysql', 'postgres', 'sqlserver', 'mongodb',
    'aws', 'azure', 'google', 'amazon', 'microsoft',
    'github', 'gitlab', 'bitbucket', 'jenkins', 'docker',
    'kubernetes', 'nginx', 'apache', 'tomcat', 'jboss',
    'wordpress', 'drupal', 'joomla', 'magento', 'shopify',
]


def load_wordlist(filepath: str = None) -> List[str]:
    """Load wordlist from file or use default"""
    if filepath and os.path.exists(filepath):
        try:
            with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                return [line.strip() for line in f if line.strip() and not line.startswith('#')]
        except Exception as e:
            logger.error(f"Error loading wordlist {filepath}: {e}")
    
    return DEFAULT_WORDLIST


def generate_mutations(word: str) -> Set[str]:
    """Generate common mutations of a word"""
    mutations = {word}
    
    # Common substitutions
    subs = {
        'a': ['@', '4'],
        'e': ['3'],
        'i': ['1', '!'],
        'o': ['0'],
        's': ['$', '5'],
        't': ['7'],
        'l': ['1'],
    }
    
    # Character substitutions
    for char, replacements in subs.items():
        if char in word.lower():
            for rep in replacements:
                mutations.add(word.replace(char, rep))
                mutations.add(word.replace(char.upper(), rep))
    
    # Append numbers
    for num in ['', '1', '12', '123', '!', '!!', '1!', '12!', '2023', '2024']:
        mutations.add(word + num)
        mutations.add(word.capitalize() + num)
        mutations.add(word.upper() + num)
    
    # Prepend numbers
    for num in ['1', '12', '123', '2023', '2024']:
        mutations.add(num + word)
    
    # Add special chars
    for special in ['!', '@', '#', '$', '%', '&', '*']:
        mutations.add(word + special)
        mutations.add(special + word)
    
    return mutations


# ═══════════════════════════════════════════════════════════════════════════
# HASH COMPUTATION FUNCTIONS
# ═══════════════════════════════════════════════════════════════════════════

def compute_md5(text: str) -> str:
    return hashlib.md5(text.encode()).hexdigest()


def compute_sha1(text: str) -> str:
    return hashlib.sha1(text.encode()).hexdigest()


def compute_sha256(text: str) -> str:
    return hashlib.sha256(text.encode()).hexdigest()


def compute_sha384(text: str) -> str:
    return hashlib.sha384(text.encode()).hexdigest()


def compute_sha512(text: str) -> str:
    return hashlib.sha512(text.encode()).hexdigest()


def compute_ntlm(text: str) -> str:
    """Compute NTLM hash (for educational purposes only)"""
    try:
        from Crypto.Hash import MD4
        from codecs import encode
        return MD4.new(encode(text, 'utf-16-le')).hexdigest()
    except ImportError:
        # Fallback using hashlib (note: this is NT hash, simplified)
        return hashlib.new('md4', text.encode('utf-16le')).hexdigest()


def verify_hash(hash_value: str, candidate: str, hash_type: str) -> bool:
    """Verify if a candidate password matches the hash"""
    hash_value = hash_value.strip().lower()
    
    try:
        if hash_type == 'MD5':
            return compute_md5(candidate).lower() == hash_value
        elif hash_type == 'SHA1':
            return compute_sha1(candidate).lower() == hash_value
        elif hash_type == 'SHA256':
            return compute_sha256(candidate).lower() == hash_value
        elif hash_type == 'SHA384':
            return compute_sha384(candidate).lower() == hash_value
        elif hash_type == 'SHA512':
            return compute_sha512(candidate).lower() == hash_value
        elif hash_type == 'NTLM':
            return compute_ntlm(candidate).lower() == hash_value
        elif hash_type == 'Base64':
            try:
                decoded = base64.b64decode(candidate).decode('utf-8', errors='ignore')
                return decoded == hash_value or candidate == hash_value
            except:
                return False
        else:
            # For salted hashes (bcrypt, argon2, etc.), we'd need the proper library
            logger.warning(f"Hash type {hash_type} requires specialized library")
            return False
    except Exception as e:
        logger.error(f"Error verifying hash: {e}")
        return False


# ═══════════════════════════════════════════════════════════════════════════
# CRACKING ENGINE
# ═══════════════════════════════════════════════════════════════════════════

class HashCracker:
    """Main hash cracking engine"""
    
    def __init__(self, wordlist_path: str = None):
        self.wordlist = load_wordlist(wordlist_path)
        self.stats = {
            'total_attempted': 0,
            'total_cracked': 0,
            'time_elapsed': 0
        }
    
    def crack_with_wordlist(self, hash_value: str, hash_type: str, 
                           use_mutations: bool = True) -> Optional[str]:
        """Attempt to crack hash using wordlist"""
        start_time = time.time()
        candidates_tried = 0
        
        # Build candidate list
        candidates = set(self.wordlist)
        
        if use_mutations:
            for word in self.wordlist[:100]:  # Limit mutations for performance
                candidates.update(generate_mutations(word))
        
        # Try each candidate
        for candidate in candidates:
            self.stats['total_attempted'] += 1
            candidates_tried += 1
            
            if verify_hash(hash_value, candidate, hash_type):
                self.stats['total_cracked'] += 1
                self.stats['time_elapsed'] = time.time() - start_time
                
                # Store in database
                self._store_cracked_hash(hash_value, hash_type, candidate, 'dictionary')
                
                logger.info(f"CRACKED: {hash_type} hash in {self.stats['time_elapsed']:.2f}s")
                return candidate
        
        self.stats['time_elapsed'] = time.time() - start_time
        return None
    
    def crack_brute_force(self, hash_value: str, hash_type: str,
                         max_length: int = 6,
                         charset: str = 'abcdefghijklmnopqrstuvwxyz0123456789') -> Optional[str]:
        """Brute force attack (limited length for performance)"""
        import itertools
        
        start_time = time.time()
        
        for length in range(1, max_length + 1):
            for candidate in itertools.product(charset, repeat=length):
                password = ''.join(candidate)
                self.stats['total_attempted'] += 1
                
                if verify_hash(hash_value, password, hash_type):
                    self.stats['total_cracked'] += 1
                    self.stats['time_elapsed'] = time.time() - start_time
                    
                    self._store_cracked_hash(hash_value, hash_type, password, 'brute_force')
                    
                    logger.info(f"BRUTE FORCE CRACKED: {password} in {self.stats['time_elapsed']:.2f}s")
                    return password
        
        return None
    
    def crack_rule_based(self, hash_value: str, hash_type: str,
                        base_words: List[str] = None) -> Optional[str]:
        """Rule-based attack using common transformations"""
        start_time = time.time()
        
        if not base_words:
            base_words = self.wordlist[:500]
        
        # Define rules
        rules = [
            lambda w: w,  # Original
            lambda w: w.upper(),
            lambda w: w.capitalize(),
            lambda w: w[::-1],  # Reversed
            lambda w: w + '1',
            lambda w: w + '123',
            lambda w: w + '!',
            lambda w: w + '2023',
            lambda w: w + '2024',
            lambda w: '1' + w,
            lambda w: '123' + w,
            lambda w: w.replace('a', '@'),
            lambda w: w.replace('e', '3'),
            lambda w: w.replace('o', '0'),
            lambda w: w.replace('s', '$'),
            lambda w: w.replace('i', '1'),
        ]
        
        for base in base_words:
            for rule in rules:
                try:
                    candidate = rule(base)
                    self.stats['total_attempted'] += 1
                    
                    if verify_hash(hash_value, candidate, hash_type):
                        self.stats['total_cracked'] += 1
                        self.stats['time_elapsed'] = time.time() - start_time
                        
                        self._store_cracked_hash(hash_value, hash_type, candidate, 'rule_based')
                        
                        return candidate
                except:
                    continue
        
        return None
    
    def _store_cracked_hash(self, hash_value: str, hash_type: str, 
                           plaintext: str, method: str):
        """Store cracked hash in database"""
        try:
            db = get_session()
            try:
                # Check if already exists
                existing = db.query(CrackedHash).filter(
                    CrackedHash.hash_value == hash_value.lower()
                ).first()
                
                if not existing:
                    cracked = CrackedHash(
                        hash_value=hash_value.lower(),
                        hash_type=hash_type,
                        plaintext=plaintext,
                        method=method,
                        wordlist_used='default' if method == 'dictionary' else None
                    )
                    db.add(cracked)
                    db.commit()
                    logger.info(f"Stored cracked hash in database: {hash_type}")
            finally:
                db.close()
        except Exception as e:
            logger.error(f"Error storing cracked hash: {e}")
    
    def get_stats(self) -> Dict:
        """Return cracking statistics"""
        return self.stats.copy()


# ═══════════════════════════════════════════════════════════════════════════
# DATABASE OPERATIONS
# ═══════════════════════════════════════════════════════════════════════════

def get_cracked_hashes(limit: int = 100, offset: int = 0) -> List[Dict]:
    """Get list of cracked hashes from database"""
    db = get_session()
    try:
        results = db.query(CrackedHash)\
            .order_by(CrackedHash.crack_time.desc())\
            .offset(offset)\
            .limit(limit)\
            .all()
        
        return [{
            'id': r.id,
            'hash_value': r.hash_value[:16] + '...' if len(r.hash_value) > 16 else r.hash_value,
            'hash_type': r.hash_type,
            'plaintext': r.plaintext,
            'method': r.method,
            'crack_time': r.crack_time.isoformat() if r.crack_time else None,
            'username': r.username,
            'source': r.source
        } for r in results]
    finally:
        db.close()


def search_cracked_hash(hash_value: str) -> Optional[Dict]:
    """Search for a specific hash in the database"""
    db = get_session()
    try:
        result = db.query(CrackedHash)\
            .filter(CrackedHash.hash_value == hash_value.lower())\
            .first()
        
        if result:
            return {
                'hash_value': result.hash_value,
                'hash_type': result.hash_type,
                'plaintext': result.plaintext,
                'method': result.method,
                'crack_time': result.crack_time.isoformat() if result.crack_time else None,
                'username': result.username,
                'source': result.source
            }
        return None
    finally:
        db.close()


def get_hash_statistics() -> Dict:
    """Get statistics about cracked hashes"""
    db = get_session()
    try:
        total = db.query(CrackedHash).count()
        
        # By type
        type_counts = db.query(
            CrackedHash.hash_type,
            sqlalchemy.func.count(CrackedHash.id)
        ).group_by(CrackedHash.hash_type).all()
        
        # By method
        method_counts = db.query(
            CrackedHash.method,
            sqlalchemy.func.count(CrackedHash.id)
        ).group_by(CrackedHash.method).all()
        
        return {
            'total_cracked': total,
            'by_type': dict(type_counts),
            'by_method': dict(method_counts)
        }
    except:
        return {'total_cracked': 0, 'by_type': {}, 'by_method': {}}
    finally:
        db.close()


# Import sqlalchemy for statistics
import sqlalchemy

# ═══════════════════════════════════════════════════════════════════════════
# INITIALIZATION
# ═══════════════════════════════════════════════════════════════════════════

def init_hash_cracker_db():
    """Create hash cracker tables"""
    Base.metadata.create_all(bind=engine)
    logger.info("Hash cracker database initialized")


if __name__ == "__main__":
    # Test the hash cracker
    print("=" * 60)
    print("ReconRadar APOLLO - Hash Cracker Module Test")
    print("=" * 60)
    
    init_hash_cracker_db()
    
    # Test hashes
    test_cases = [
        ('5f4dcc3b5aa765d61d8327deb882cf99', 'MD5'),  # password
        ('7c4a8d09ca3762af61e59520943dc26494f8941b', 'SHA1'),  # 1234567890
        ('5e884898da28047151d0e56f8dc6292773603d0d6aabbdd62a11ef721d1542d8', 'SHA256'),  # password
    ]
    
    cracker = HashCracker()
    
    for hash_val, hash_type in test_cases:
        print(f"\nAttempting to crack {hash_type}: {hash_val[:20]}...")
        result = cracker.crack_with_wordlist(hash_val, hash_type)
        if result:
            print(f"✓ CRACKED! Plaintext: {result}")
        else:
            print(f"✗ Not cracked with current wordlist")
    
    print("\n" + "=" * 60)
    print(f"Statistics: {cracker.get_stats()}")
    print("=" * 60)
