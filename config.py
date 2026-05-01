"""
Project Indolance — Configuration
================================
Central configuration for scan paths, API endpoints, regex patterns, and analysis settings.
"""

import os

# ─── Base Paths ──────────────────────────────────────────────────────────────
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")
STATIC_IMG_DIR = os.path.join(BASE_DIR, "static", "img")
SAMPLE_DIR = os.path.join(BASE_DIR, "sample_files")

# Ensure runtime directories exist
os.makedirs(DATA_DIR, exist_ok=True)
os.makedirs(STATIC_IMG_DIR, exist_ok=True)

# ─── Part A: Local Reader Settings ──────────────────────────────────────────
# Directories to scan for local files (add your own paths here)
SCAN_DIRECTORIES = [
    SAMPLE_DIR,
    # r"C:\Users\YourName\Documents\Research",
    # r"C:\Users\YourName\Projects",
]

# Supported file extensions
SUPPORTED_EXTENSIONS = {
    ".pdf",       # Research papers, IEEE drafts
    ".py",        # Python source code
    ".c", ".cpp", ".h",  # C/C++ source code
    ".tex",       # LaTeX documents
    ".md",        # Markdown notes
    ".txt",       # Plain text
    ".java",      # Java source code
    ".js",        # JavaScript source code
    ".rs",        # Rust source code
}

# Domain-specific keyword patterns (regex)
# These will be matched case-insensitively in extracted text
DOMAIN_KEYWORD_PATTERNS = [
    # Security Hardware & Chips
    r"ATECC608[AB]?",
    r"TPM\s*2\.0",
    r"HSM",

    # Networking & Protocols
    r"PCAP",
    r"IEEE\s*802\.\d+\w*",
    r"TCP/IP",
    r"MQTT",
    r"CoAP",
    r"Zigbee",
    r"LoRa(?:WAN)?",
    r"Bluetooth\s*(?:LE|Low\s*Energy)?",
    r"Wi-?Fi",

    # AI & Machine Learning
    r"(?:deep|machine)\s*learning",
    r"neural\s*network",
    r"CNN|RNN|LSTM|GAN|transformer",
    r"TensorFlow|PyTorch|Keras",
    r"reinforcement\s*learning",
    r"natural\s*language\s*processing|NLP",
    r"computer\s*vision",

    # IoT & Embedded
    r"IoT",
    r"Raspberry\s*Pi",
    r"Arduino",
    r"ESP32|ESP8266",
    r"FPGA",
    r"RTOS",
    r"embedded\s*system",

    # Security Concepts
    r"encryption|AES|RSA|ECC",
    r"firewall",
    r"intrusion\s*detection",
    r"penetration\s*testing",
    r"zero[\s-]*trust",
    r"blockchain",

    # Cloud & DevOps
    r"Docker|Kubernetes|K8s",
    r"AWS|Azure|GCP",
    r"microservice",
    r"CI/CD",
    r"serverless",

    # Data & Analytics
    r"big\s*data",
    r"data\s*pipeline",
    r"ETL",
    r"data\s*lake",

    # Emerging Tech
    r"quantum\s*computing",
    r"edge\s*computing",
    r"digital\s*twin",
    r"5G|6G",
    r"AR|VR|XR",
    r"autonomous\s*vehicle",
]

# ─── Part B: API-Based Search Settings ──────────────────────────────────────
# Semantic Scholar — Free, no auth needed, 100 req/5min
SEMANTIC_SCHOLAR_API = "https://api.semanticscholar.org/graph/v1/paper/search"
SEMANTIC_SCHOLAR_FIELDS = "title,abstract,url,year,citationCount,externalIds"
SEMANTIC_SCHOLAR_LIMIT = 15  # results per query

# CrossRef — Free, no auth needed
CROSSREF_API = "https://api.crossref.org/works"
CROSSREF_LIMIT = 10  # results per query

# GitHub Search — Free, 10 req/min unauthenticated, 30 req/min with token
GITHUB_SEARCH_API = "https://api.github.com/search/repositories"
GITHUB_LIMIT = 15  # results per query
GITHUB_TOKEN = ""  # Optional: set your GitHub personal access token for higher rate limits

# OpenAlex — Free, no auth needed, very generous limits
OPENALEX_API = "https://api.openalex.org/works"
OPENALEX_LIMIT = 15

# Rate limiting between API calls
API_DELAY_MIN = 0.5   # Minimum seconds between requests
API_DELAY_MAX = 1.5   # Maximum seconds between requests

# User-Agent for API requests (polite identification)
API_USER_AGENT = "ProjectIndolance/1.0 (Research Originality Checker; mailto:student@example.com)"

# ─── Part C: Comparison Engine Settings ─────────────────────────────────────
# Local similarity thresholds
LOCAL_SIMILARITY_HIGH = 0.6     # Above this = "Heavily Overlapping"
LOCAL_SIMILARITY_MEDIUM = 0.25  # Between medium and high = "Some Overlap"
                                # Below medium = "Original"

# Global similarity thresholds
GLOBAL_SIMILARITY_HIGH = 0.5    # Above this = "Already Exists"
GLOBAL_SIMILARITY_MEDIUM = 0.2  # Between medium and high = "Similar Work Found"
                                # Below medium = "Potentially Original"

# Plagiarism source threshold — include sources above this similarity
PLAGIARISM_SOURCE_THRESHOLD = 0.15

# Top N gap suggestions to show
TOP_GAP_SUGGESTIONS = 10

# ─── Flask Settings ─────────────────────────────────────────────────────────
FLASK_HOST = "0.0.0.0"
FLASK_PORT = 5000
FLASK_DEBUG = True
