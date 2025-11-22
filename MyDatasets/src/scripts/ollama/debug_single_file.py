#!/usr/bin/env python
# debug_single_file.py
# for debugging the scanning process on a single file

import sys
import traceback
from scanner import VulnerabilityScanner

def debug_scan(file_path):
    """Debug the scanning process on a single file"""
    print("=" * 60)
    print("Debugging single file scan")
    print("=" * 60)
    print(f"File: {file_path}\n")
    
    scanner = VulnerabilityScanner()
    
    try:
        # Step 1: Read file content
        print("Step 1: Reading file content...")
        code = scanner.read_file(file_path)
        print(f"✓ File read successfully ({len(code)} characters)")
        print(f"First 100 characters: {code[:100]}...\n")
        
        # Step 2: Construct prompt
        print("Step 2: Constructing prompt...")
        from config import VULNERABILITY_PROMPT
        prompt = VULNERABILITY_PROMPT.format(code_content=code[:500])  # Only use the first 500 characters for testing
        print(f"✓ Prompt constructed successfully ({len(prompt)} characters)\n")
        
        # Step 3: Call API
        print("Step 3: Calling Ollama API...")
        import requests
        from config import OLLAMA_API_URL, MODEL_NAME
        
        payload = {
            "model": MODEL_NAME,
            "prompt": prompt,
            "stream": False,
            "temperature": 0.1
        }
        
        response = requests.post(OLLAMA_API_URL, json=payload, timeout=60)
        print(f"✓ API response status code: {response.status_code}\n")
        
        # Step 4: Parse response
        print("Step 4: Parsing response...")
        result = response.json()
        print(f"Response keys: {result.keys()}")
        print(f"\nFull response:")
        print(result)
        
        if 'response' in result:
            print(f"\nModel reply:")
            print(result['response'][:500])
        
    except Exception as e:
        print(f"\n✗ Error occurred!")
        print(f"Error type: {type(e).__name__}")
        print(f"Error message: {e}")
        print(f"\nFull stack trace:")
        traceback.print_exc()

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python debug_single_file.py <file_path>")
        print("For example: python debug_single_file.py ../../dataset_01/bad_code_clean/CWE121_xxx.c")
        sys.exit(1)
    
    debug_scan(sys.argv[1])