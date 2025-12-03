# scanner.py
# Recommended version for academic research - reliable JSON parsing

import requests
import json
import os
from pathlib import Path
from datetime import datetime
import time
import re
from config import (
    OLLAMA_API_URL, MODEL_NAME, VULNERABILITY_PROMPT,
    DELAY_BETWEEN_FILES, REQUEST_TIMEOUT, OUTPUT_DIR
)

class VulnerabilityScanner:
    def __init__(self):
        self.api_url = OLLAMA_API_URL
        self.model_name = MODEL_NAME
        self.scan_count = 0
        self.success_count = 0
        self.fail_count = 0
    
    def read_file(self, file_path):
        """Read file with encoding fallback"""
        for encoding in ['utf-8', 'gbk', 'latin-1']:
            try:
                with open(file_path, 'r', encoding=encoding) as f:
                    return f.read()
            except UnicodeDecodeError:
                continue
        raise Exception("Cannot read file with common encodings")
    
    def parse_llm_response(self, response_text):
        """Parse JSON response from LLM with robust error handling"""
        json_data = None
        
        # Method 1: Remove markdown code blocks (```json ... ```)
        if '```' in response_text:
            try:
                # Extract content between ```json and ```
                pattern = r'```(?:json)?\s*([\s\S]*?)```'
                matches = re.findall(pattern, response_text)
                if matches:
                    for match in matches:
                        try:
                            json_data = json.loads(match.strip())
                            if isinstance(json_data, dict) and 'has_vulnerability' in json_data:
                                break
                        except:
                            continue
            except:
                pass
        
        # Method 2: Try to parse the entire response as JSON (after stripping)
        if json_data is None:
            try:
                cleaned = response_text.strip()
                json_data = json.loads(cleaned)
            except:
                pass
        
        # Method 3: Find JSON object anywhere in text
        if json_data is None:
            try:
                # Find { ... } pattern
                start = response_text.find('{')
                if start != -1:
                    # Find matching closing brace
                    brace_count = 0
                    end = start
                    for i in range(start, len(response_text)):
                        if response_text[i] == '{':
                            brace_count += 1
                        elif response_text[i] == '}':
                            brace_count -= 1
                            if brace_count == 0:
                                end = i + 1
                                break
                    
                    if end > start:
                        json_str = response_text[start:end]
                        json_data = json.loads(json_str)
            except:
                pass
        
        # If we successfully extracted JSON, validate and return
        if json_data and isinstance(json_data, dict):
            try:
                # Check if it has the expected fields
                if 'has_vulnerability' in json_data:
                    return {
                        'parsed': True,
                        'has_vulnerability': bool(json_data.get('has_vulnerability', False)),
                        'vulnerability_type': str(json_data.get('vulnerability_type', 'unknown')),
                        'line_numbers': list(json_data.get('line_numbers', [])),
                        'severity': str(json_data.get('severity', 'unknown')),
                        'description': str(json_data.get('description', ''))[:1000],
                        'secure_fix': str(json_data.get('secure_fix', ''))[:2000],
                        'confidence': int(json_data.get('confidence', 0))
                    }
            except Exception as e:
                pass
        
        # Fallback: keyword detection
        response_lower = response_text.lower()
        has_vuln = any(kw in response_lower for kw in 
                      ['buffer overflow', 'vulnerable', 'overflow', 'gets(', 'strcpy'])
        
        return {
            'parsed': False,
            'has_vulnerability': has_vuln,
            'vulnerability_type': 'unknown',
            'line_numbers': [],
            'severity': 'unknown',
            'description': response_text[:500],
            'secure_fix': '',
            'confidence': 30,
            'parse_error': 'Failed to parse JSON from response'
        }
    
    def scan_single_file(self, file_path):
        """Scan a single file"""
        self.scan_count += 1
        
        result = {
            'file': str(file_path),
            'file_name': Path(file_path).name,
            'scan_number': self.scan_count,
            'timestamp': datetime.now().isoformat(),
            'success': False
        }
        
        try:
            code = self.read_file(file_path)
            result['file_size'] = len(code)
            result['line_count'] = code.count('\n') + 1
            
            # Build prompt
            prompt = VULNERABILITY_PROMPT.replace('{code_content}', code)
            
            # Call API
            payload = {
                "model": self.model_name,
                "prompt": prompt,
                "stream": False,
                "temperature": 0.1
            }
            
            response = requests.post(self.api_url, json=payload, timeout=REQUEST_TIMEOUT)
            response.raise_for_status()
            
            llm_result = response.json()
            model_response = llm_result['response']
            
            # Parse response
            parsed = self.parse_llm_response(model_response)
            
            result.update({
                'success': True,
                'model_response': model_response,
                'analysis': parsed
            })
            
            self.success_count += 1
            
        except requests.exceptions.Timeout:
            result['error'] = 'API request timed out'
            self.fail_count += 1
        except requests.exceptions.ConnectionError:
            result['error'] = 'Failed to connect to Ollama'
            self.fail_count += 1
        except Exception as e:
            result['error'] = str(e)
            self.fail_count += 1
        
        return result
    
    def scan_directory(self, directory, pattern='*.c', max_files=None):
        """Scan directory"""
        directory_path = Path(directory)
        if not directory_path.exists():
            raise FileNotFoundError(f"Directory not found: {directory}")
        
        all_files = list(directory_path.rglob(pattern))
        
        if not all_files:
            print(f"Warning: No {pattern} files found")
            return []
        
        if max_files and max_files < len(all_files):
            files = all_files[:max_files]
            print(f"\nFound {len(all_files)} files, scanning first {max_files}")
        else:
            files = all_files
            print(f"\nFound {len(files)} files to scan")
        
        print("=" * 60)
        
        results = []
        
        for i, file_path in enumerate(files, 1):
            print(f"\n[{i}/{len(files)}] Scanning: {file_path.name}")
            
            result = self.scan_single_file(file_path)
            results.append(result)
            
            if result['success']:
                analysis = result['analysis']
                parsed = analysis.get('parsed', False)
                has_vuln = analysis.get('has_vulnerability', False)
                
                if has_vuln:
                    vtype = analysis.get('vulnerability_type', 'unknown')
                    severity = analysis.get('severity', 'unknown')
                    print(f"  ⚠ VULNERABLE - {vtype} ({severity})")
                    if parsed:
                        print(f"  ✓ JSON parsed successfully")
                    else:
                        print(f"  ⚠ JSON parse failed, used keyword detection")
                else:
                    print(f"  ✓ Clean")
            else:
                print(f"  ✗ Error: {result.get('error')}")
            
            if i < len(files):
                time.sleep(DELAY_BETWEEN_FILES)
        
        return results
    
    def save_results(self, results, output_file=None):
        """Save results"""
        os.makedirs(OUTPUT_DIR, exist_ok=True)
        
        if output_file is None:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            output_file = os.path.join(OUTPUT_DIR, f'scan_results_{timestamp}.json')
        
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(results, f, indent=2, ensure_ascii=False)
        
        print("\n" + "=" * 60)
        print("Scan Complete!")
        print("=" * 60)
        print(f"Total files: {len(results)}")
        print(f"Successful scans: {self.success_count}")
        print(f"Failed scans: {self.fail_count}")
        
        # Parse statistics
        parsed_count = sum(1 for r in results 
                          if r.get('success') and r.get('analysis', {}).get('parsed'))
        if self.success_count > 0:
            print(f"JSON parsed successfully: {parsed_count}/{self.success_count} ({parsed_count/self.success_count*100:.1f}%)")
        
        vuln_count = sum(1 for r in results 
                        if r.get('success') and r.get('analysis', {}).get('has_vulnerability'))
        print(f"Vulnerabilities detected: {vuln_count}")
        print(f"Results saved to: {output_file}")

        # Count vulnerabilities
        vuln_count = sum(1 for r in results
                        if r.get('success') and 
                        r.get('analysis', {}).get('has_vulnerability', False))
        print(f"Vulnerable files detected: {vuln_count}")

        return output_file
