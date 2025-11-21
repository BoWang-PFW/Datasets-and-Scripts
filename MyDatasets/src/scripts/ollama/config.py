# config.py
# usage: Configuration file for Ollama-based C/C++ vulnerability scanner

# configure Ollama API settings
OLLAMA_API_URL = "http://localhost:11434/api/generate"
MODEL_NAME = "codellama:7b-instruct-q4_0"

# scan configuration
SCAN_PATTERN = "*.c"  # can be changed to "*.cpp" or other patterns
DELAY_BETWEEN_FILES = 1  # seconds to wait between each file
REQUEST_TIMEOUT = 120  # API request timeout in seconds

# Prompt template for vulnerability scanning
VULNERABILITY_PROMPT = """Find security vulnerabilities in this code:

{code_content}

JSON output:
{{
  "vulnerable": true/false,
  "type": "vulnerability_type",
  "line": 0,
  "reason": "brief"
}}"""
# output configuration
OUTPUT_DIR = "results"
SAVE_INDIVIDUAL_FILES = True  # whether to save results for each scanned file individually
