# scanner.py
# usage: Ollama-based C/C++ vulnerability scanner implementation

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
    # initialize scanner
    def __init__(self):
        self.api_url = OLLAMA_API_URL
        self.model_name = MODEL_NAME
        self.scan_count = 0
        self.success_count = 0
        self.fail_count = 0
    
    def read_file(self, file_path):
        # read file content with multiple encoding attempts
        encodings = ['utf-8', 'gbk']
        
        for encoding in encodings:
            try:
                with open(file_path, 'r', encoding=encoding) as f:
                    return f.read()
            except UnicodeDecodeError:
                continue
            except Exception as e:
                raise Exception(f"Cannot read file: {e}")

        raise Exception("Cannot read file with common encodings")

    def parse_llm_response(self, response_text):
        # parse LLM response to extract vulnerability info
        try:
            # Try to extract JSON part from the response
            json_match = re.search(r'\{[^{}]*"has_vulnerability"[^{}]*\}', response_text, re.DOTALL)
            if json_match:
                json_str = json_match.group()
                data = json.loads(json_str)
                return {
                    'parsed': True,
                    'has_vulnerability': data.get('has_vulnerability', False),
                    'vulnerability_type': data.get('vulnerability_type', 'unknown'),
                    'line_numbers': data.get('line_numbers', []),
                    'severity': data.get('severity', 'unknown'),
                    'description': data.get('description', ''),
                    'confidence': data.get('confidence', 0)
                }
        except Exception as e:
            pass
        
        # If JSON parsing fails, use keyword detection
        response_lower = response_text.lower()
        keywords = ['buffer overflow', 'vulnerable', 'vulnerability', 'overflow', 'gets(']
        has_vuln = any(keyword in response_lower for keyword in keywords)
        
        return {
            'parsed': False,
            'has_vulnerability': has_vuln,
            'raw_response': response_text[:500],  # only keep first 500 chars
            'note': 'Failed to parse JSON, used keyword detection'
        }
    
    def scan_single_file(self, file_path):
        # scan a single file for vulnerabilities
        self.scan_count += 1
        
        result = {
            'file': str(file_path),
            'file_name': Path(file_path).name,
            'scan_number': self.scan_count,
            'timestamp': datetime.now().isoformat(),
            'success': False
        }
        
        try:
            # read code
            code_content = self.read_file(file_path)
            result['file_size'] = len(code_content)
            result['line_count'] = code_content.count('\n') + 1
            
            # construct prompt
            prompt = VULNERABILITY_PROMPT.replace("{code_content}", code_content)


            # call API
            payload = {
                "model": self.model_name,
                "prompt": prompt,
                "stream": False,
                "temperature": 0.1
            }
            
            response = requests.post(
                self.api_url, 
                json=payload, 
                timeout=REQUEST_TIMEOUT
            )
            response.raise_for_status()
            
            # parse response
            llm_result = response.json()
            model_response = llm_result['response']

            # parse LLM response
            parsed_result = self.parse_llm_response(model_response)
            
            result.update({
                'success': True,
                'model_response': model_response,
                'analysis': parsed_result
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
        """scan all files in a directory matching the pattern
        
        Args:
            directory: the directory path to scan
            pattern: file matching pattern
            max_files: maximum number of files to scan (for test mode)
        """
        # Find all files matching the pattern
        directory_path = Path(directory)
        if not directory_path.exists():
            raise FileNotFoundError(f"Directory does not exist: {directory}")

        all_files = list(directory_path.rglob(pattern))
        
        if not all_files:
            print(f"Warning: No {pattern} files found in {directory}")
            return []
        
        # if set max_files, limit the number of files to scan
        if max_files and max_files < len(all_files):
            files = all_files[:max_files]
            print(f"\nFound {len(all_files)} files, test mode will scan the first {max_files} files")
        else:
            files = all_files
            print(f"\nFound {len(files)} files to scan")

        print("=" * 60)
        
        results = []
        
        for i, file_path in enumerate(files, 1):
            print(f"\n[{i}/{len(files)}] Scanning: {file_path.name}")
            print(f"  Path: {file_path}")

            # Scan file
            result = self.scan_single_file(file_path)
            results.append(result)

            # Show results
            if result['success']:
                analysis = result['analysis']
                has_vuln = analysis.get('has_vulnerability', False)
                status = "Vulnerability found" if has_vuln else "No vulnerability found"
                print(f"  Status: {status}")
                
                if has_vuln and 'description' in analysis:
                    print(f"  Description: {analysis['description'][:80]}")
            else:
                print(f" !Error: {result.get('error', 'Unknown error')}")

            # Delay between files
            if i < len(files):
                time.sleep(DELAY_BETWEEN_FILES)
        
        return results
    
    def save_results(self, results, output_file=None):
        """Save scan results to a JSON file"""
        # make sure output directory exists
        os.makedirs(OUTPUT_DIR, exist_ok=True)

        # generate file name with timestamp if not provided
        if output_file is None:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            output_file = os.path.join(OUTPUT_DIR, f'scan_results_{timestamp}.json')

        # Save JSON file
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(results, f, indent=2, ensure_ascii=False)
        
        print("\n" + "=" * 60)
        print("Scan complete!")
        print("=" * 60)
        print(f"Total files scanned: {len(results)}")
        print(f"Success: {self.success_count}")
        print(f"Failed: {self.fail_count}")
        print(f"Results saved to: {output_file}")

        # Count vulnerabilities
        vuln_count = sum(1 for r in results
                        if r.get('success') and 
                        r.get('analysis', {}).get('has_vulnerability', False))
        print(f"Vulnerable files detected: {vuln_count}")

        return output_file
