# config_commercial.py
# Usage：Configuration file of commercial LLMs（Claude, ChatGPT, Gemini)

import os
from pathlib import Path

# load .env file if exists
try:
    from dotenv import load_dotenv
    env_path = Path(__file__).parent / '.env'
    if env_path.exists():
        load_dotenv(env_path)
        print("Loaded .env file for commercial LLM configuration")
    else:
        load_dotenv()  # load from default .env in current directory
except ImportError:
    print("python-dotenv not installed, skipping .env loading")
    print("Run: pip install python-dotenv")

# select LLM provider
# options: "claude", "chatgpt", "gemini"
LLM_PROVIDER = "claude"  # change here to switch LLM

# API Keys for commercial LLMs
# Method 1: Directly fill in here (not recommended, easy to leak)
# CLAUDE_API_KEY = ""  # Fill in your Claude API key
# CHATGPT_API_KEY = ""  # Fill in your OpenAI API key
# GEMINI_API_KEY = ""   # Fill in your Google API key

# Method 2: Load from environment variables (recommended)
CLAUDE_API_KEY = os.getenv("CLAUDE_API_KEY", "")
CHATGPT_API_KEY = os.getenv("OPENAI_API_KEY", "")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")

# configurations for different LLMs
MODEL_CONFIGS = {
    "claude": {
        "model_name": "claude-sonnet-4-20250514",  # latest Sonnet 4
        "max_tokens": 4096,
        "temperature": 0.1
    },
    "chatgpt": {
        "model_name": "gpt-4o",  # or "gpt-4o-mini", "gpt-4-turbo"
        "max_tokens": 4096,
        "temperature": 0.1
    },
    "gemini": {
        "model_name": "gemini-1.5-pro",  # or "gemini-1.5-flash"
        "max_tokens": 4096,
        "temperature": 0.1
    }
}

# configurations for file scanning
SCAN_PATTERN = "*.c"
DELAY_BETWEEN_FILES = 1  # Commercial APIs are faster, so delay can be reduced
REQUEST_TIMEOUT = 60

# Prompt templates
VULNERABILITY_PROMPT = """You are a security code analyzer. Analyze the following C/C++ code ONLY for buffer overflow vulnerabilities.

Code:
```c
{code_content}
```

Respond in this EXACT JSON format (no extra text):
{{
  "has_vulnerability": true,
  "vulnerability_type": "buffer_overflow",
  "line_numbers": [12, 15],
  "severity": "high",
  "description": "Brief description of the vulnerability",
  "confidence": 85
}}

If NO vulnerability found, respond:
{{
  "has_vulnerability": false,
  "vulnerability_type": "none",
  "line_numbers": [],
  "severity": "none",
  "description": "No buffer overflow detected",
  "confidence": 90
}}"""

# Output directory for results
OUTPUT_DIR = "results_commercial"