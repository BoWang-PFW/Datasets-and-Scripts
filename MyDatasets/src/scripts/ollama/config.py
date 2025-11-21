# config.py
# usage: Configuration file for Ollama-based C/C++ vulnerability scanner

# configure Ollama API settings
OLLAMA_API_URL = "http://localhost:11434/api/generate"
MODEL_NAME = "codellama:7b-instruct-q4_0"

# scan configuration
SCAN_PATTERN = "*.c"  # can be changed to "*.cpp" or other patterns
DELAY_BETWEEN_FILES = 2  # seconds to wait between each file
REQUEST_TIMEOUT = 60  # API request timeout in seconds

# Prompt template for vulnerability scanning
VULNERABILITY_PROMPT = """You are an expert security code reviewer. For each code snippet below, perform a thorough security analysis. 
 
For each snippet, follow these steps: 
1. Examine the code for common security vulnerabilities 
2. Determine if a vulnerability exists 
3. If found, identify the root cause and potential impact 
4. Provide a secure implementation 
 
Response format: 
**SNIPPET [number]:** 
**Vulnerability:** [YES/NO] 
**Type:** [specific vulnerability name or "None detected"] 
**Explanation:** [Describe what makes this code vulnerable and the potential security impact in 2-3 sentences] 
**Secure Code:** 
``` 
[Fixed code with inline comments explaining security improvements, or "No changes required"] 
``` 
 
**Example Analysis:** 
**SNIPPET 1:** 
```python 
username = request.GET['user'] 
query = f"SELECT * FROM users WHERE name = '{username}'" 
cursor.execute(query) 
``` 
 
**Vulnerability:** YES 
**Type:** SQL Injection 
**Explanation:** User input is directly concatenated into the SQL query without sanitization. An attacker could inject `'; DROP TABLE users; --` to execute arbitrary SQL commands, potentially destroying data or exposing sensitive information. 
**Secure Code:** 
```python 
# Use parameterized queries to prevent SQL injection 
username = request.GET['user'] 
query = "SELECT * FROM users WHERE name = %s"  # Parameterized placeholder 
cursor.execute(query, (username,))  # Pass user input as separate parameter 
``` 
--- 
 
Now analyze the following snippets: """

# output configuration
OUTPUT_DIR = "results"
SAVE_INDIVIDUAL_FILES = True  # whether to save results for each scanned file individually