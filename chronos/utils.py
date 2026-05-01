"""
Project Indolance — Utilities
=============================
Shared helpers for text cleaning, stopwords, logging, and file detection.
"""

import re
import logging
import os
from datetime import datetime

# ─── Logging Setup ──────────────────────────────────────────────────────────

def setup_logger(name="chronos", level=logging.INFO):
    """Create a configured logger instance."""
    logger = logging.getLogger(name)
    if not logger.handlers:
        handler = logging.StreamHandler()
        formatter = logging.Formatter(
            "[%(asctime)s] %(name)s — %(levelname)s — %(message)s",
            datefmt="%H:%M:%S"
        )
        handler.setFormatter(formatter)
        logger.addHandler(handler)
    logger.setLevel(level)
    return logger

logger = setup_logger()

# ─── Stopwords ──────────────────────────────────────────────────────────────

# Common English stopwords + technical noise words
STOPWORDS = {
    # English common words
    "the", "a", "an", "and", "or", "but", "in", "on", "at", "to", "for",
    "of", "with", "by", "from", "is", "it", "as", "be", "this", "that",
    "are", "was", "were", "been", "has", "have", "had", "do", "does",
    "did", "will", "would", "could", "should", "may", "might", "can",
    "shall", "not", "no", "if", "then", "than", "so", "just", "also",
    "more", "most", "such", "when", "where", "which", "who", "whom",
    "how", "what", "why", "all", "each", "every", "both", "few", "many",
    "some", "any", "other", "into", "through", "during", "before",
    "after", "above", "below", "between", "out", "off", "over", "under",
    "again", "further", "once", "here", "there", "about", "up", "very",
    "own", "same", "only", "its", "our", "your", "their", "we", "you",
    "he", "she", "they", "me", "him", "her", "us", "them", "my", "his",
    "being", "having", "doing", "while", "until", "because", "although",
    # Technical noise words
    "using", "based", "approach", "method", "system", "proposed",
    "paper", "results", "study", "research", "analysis", "data",
    "model", "used", "new", "first", "two", "one", "time", "however",
    "since", "well", "even", "still", "need", "get", "make", "like",
    "use", "set", "see", "way", "work", "part", "case", "take",
    "come", "good", "give", "say", "help", "tell", "try", "show",
    "know", "want", "look", "find", "think", "let", "keep", "end",
    "put", "run", "begin", "seem", "call", "turn", "ask", "go",
    "number", "people", "long", "day", "thing", "man", "world", "life",
    "hand", "high", "place", "year", "back", "point", "type", "home",
    "small", "large", "next", "early", "young", "important", "public",
    "must", "right", "left", "old", "big", "great", "different",
    "another", "around", "possible", "available", "particular",
    "second", "last", "certain", "form", "present", "include",
    "provide", "require", "without", "within", "according",
    "among", "across", "along", "already", "rather", "whether",
    "often", "much", "always", "example", "several", "among",
    "upon", "thus", "therefore", "hence", "per", "via", "etc",
    "def", "return", "import", "class", "self", "none", "true", "false",
    "print", "else", "elif", "pass", "break", "continue", "lambda",
    "try", "except", "finally", "raise", "assert", "yield", "global",
    "del", "exec", "eval", "file", "open", "read", "write", "close",
    "line", "function", "variable", "value", "string", "list", "dict",
    "int", "float", "bool", "str", "len", "range", "enumerate",
}


# ─── Text Cleaning ──────────────────────────────────────────────────────────

def clean_text(text):
    """
    Clean raw text for keyword extraction.

    - Removes URLs
    - Removes email addresses
    - Removes excessive special characters
    - Normalizes whitespace
    - Converts to lowercase
    """
    if not text:
        return ""

    # Remove URLs
    text = re.sub(r'https?://\S+|www\.\S+', ' ', text)
    # Remove email addresses
    text = re.sub(r'\S+@\S+\.\S+', ' ', text)
    # Remove non-alphanumeric characters (keep hyphens, slashes for terms like TCP/IP)
    text = re.sub(r'[^a-zA-Z0-9\s/\-\.]', ' ', text)
    # Normalize whitespace
    text = re.sub(r'\s+', ' ', text).strip()

    return text


def extract_words(text, min_length=3):
    """
    Extract meaningful words from text, removing stopwords and short tokens.

    Returns a list of lowercase words.
    """
    text = clean_text(text)
    words = re.findall(r'[a-zA-Z][a-zA-Z0-9\-]{2,}', text.lower())
    return [w for w in words if w not in STOPWORDS and len(w) >= min_length]


# ─── File Helpers ────────────────────────────────────────────────────────────

def get_file_timestamp(filepath):
    """Get the last-modified timestamp of a file as ISO string."""
    try:
        mtime = os.path.getmtime(filepath)
        return datetime.fromtimestamp(mtime).isoformat()
    except OSError:
        return datetime.now().isoformat()


def get_file_extension(filepath):
    """Get the lowercase file extension."""
    return os.path.splitext(filepath)[1].lower()


def is_binary_file(filepath):
    """Quick check if a file appears to be binary."""
    try:
        with open(filepath, 'rb') as f:
            chunk = f.read(1024)
            if b'\x00' in chunk:
                return True
            return False
    except (OSError, IOError):
        return True


def truncate_text(text, max_length=200):
    """Truncate text to a maximum length, adding ellipsis if needed."""
    if len(text) <= max_length:
        return text
    return text[:max_length - 3] + "..."
