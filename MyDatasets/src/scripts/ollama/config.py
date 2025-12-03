# config.py
# Recommended configuration for academic research

OLLAMA_API_URL = "http://localhost:11434/api/generate"
MODEL_NAME = "codellama:7b-instruct-q4_0"

SCAN_PATTERN = "*.c"
DELAY_BETWEEN_FILES = 0.5
REQUEST_TIMEOUT = 120

# Simplified prompt for better JSON compliance
VULNERABILITY_PROMPT = """Analyze for buffer overflow. Output JSON only, explain in one sentence.

Example input:
```c
char buf[10]; strcpy(buf, input);
```

Example output:
{{"has_vulnerability": true, "vulnerability_type": "buffer_overflow", "line_numbers": [1], "severity": "high", "description": "strcpy no bounds check", "secure_fix": "use strncpy", "confidence": 90}}

Code to analyze:
{code_content}

JSON:"""

OUTPUT_DIR = "results"
SAVE_INDIVIDUAL_FILES = True
