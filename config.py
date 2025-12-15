"""Configuration settings for the Competitor Analyzer"""
import os
from dotenv import load_dotenv

load_dotenv()

# API Configuration
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
PROXY_API_KEY = os.getenv("PROXY_API_KEY")
PROXY_API_URL = os.getenv("PROXY_API_URL")

# Use Proxy API if configured, otherwise use OpenAI
USE_PROXY = bool(PROXY_API_KEY and PROXY_API_URL)

# Competitor URLs for parsing
COMPETITOR_URLS = [
    "https://example-competitor1.com",
    "https://example-competitor2.com",
    "https://example-competitor3.com",
]

# History storage
HISTORY_DIR = "history"
os.makedirs(HISTORY_DIR, exist_ok=True)

# Selenium Configuration
SELENIUM_HEADLESS = True
SELENIUM_TIMEOUT = 30

# API Configuration
API_HOST = "0.0.0.0"
API_PORT = 8000

