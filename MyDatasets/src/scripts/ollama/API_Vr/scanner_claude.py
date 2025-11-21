# scanner_claude.py
# Usage: Claude-based vulnerability scanner (minimal changes from original)

import json
import os
from pathlib import Path
from datetime import datetime
import time
import anthropic
from config import DELAY_BETWEEN_FILES, OUTPUT_DIR

class VulnerabilityScannerClaude:
    def __init__(self, api_key, model="claude-3-5-haiku-20241022"):
        """
        Args:
            api_key: Anthropic API key
            model: Model name (haiku is fast/cheap, sonnet is more accurate)
        """
        self.client = anthropic.Anthropic(api_key=api_key)
        self.model = model
        self.scan_count = 0
        self.success_count = 0
        self.fail_count = 0
        
        self.prompt_template = """Analyze this C/C++ code for buffer overflow vulnerabilities.

Code:
{code_content}

Respond in JSON format:
{{
  "has_vulnerability": true or false,
  "vulnerability_type": "buffer_overflow" or "none",
  "line_numbers": [],
  "severity": "high/medium/low/none",
  "description": "brief explanation",
  "confidence": 0-100
}}"""
    
    def read_file(self, file_path):
        """Read file with encoding fallback"""
        for encoding in ['utf-8', 'gbk', 'latin-1']:
            try:
                with open(file_path, 'r', encoding=encoding) as f:
                    return f.read()
            except UnicodeDecodeError:
                continue
        raise Exception("Cannot read file with common encodings")
    
    def parse_response(self, response_text):
        """Parse JSON response"""
        try:
            start = response_text.find('{')
            end = response_text.rfind('}') + 1
            if start != -1 and end > start:
                json_str = response_text[start:end]
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
        except:
            pass
        
        response_lower = response_text.lower()
        has_vuln = any(kw in response_lower for kw in 
                      ['buffer overflow', 'vulnerable', 'overflow'])
        return {
            'parsed': False,
            'has_vulnerability': has_vuln,
            'raw_response': response_text[:500]
        }
    
    def scan_single_file(self, file_path):
        """Scan a single file"""
        self.scan_count += 1
        result = {
            'file': str(file_path),
            'file_name': Path(file_path).name,
            'scan_number': self.scan_count,
            'timestamp': datetime.now().isoformat(),
            'success': False,
            'api_used': f'Anthropic {self.model}'
        }
        
        try:
            code = self.read_file(file_path)
            result['file_size'] = len(code)
            result['line_count'] = code.count('\n') + 1
            
            # Limit code length
            if len(code) > 8000:
                code = code[:8000]
                result['note'] = 'Code truncated to 8000 chars'
            
            prompt = self.prompt_template.replace('{code_content}', code)
            
            # Call Claude API
            message = self.client.messages.create(
                model=self.model,
                max_tokens=1024,
                temperature=0.1,
                messages=[{"role": "user", "content": prompt}]
            )
            
            response_text = message.content[0].text
            parsed = self.parse_response(response_text)
            
            result.update({
                'success': True,
                'model_response': response_text,
                'analysis': parsed,
                'tokens_used': message.usage.input_tokens + message.usage.output_tokens
            })
            self.success_count += 1
            
        except Exception as e:
            result['error'] = str(e)
            self.fail_count += 1
        
        return result
    
    def scan_directory(self, directory, pattern='*.c', max_files=None):
        """Scan directory (same interface)"""
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
                vuln = result['analysis'].get('has_vulnerability', False)
                status = "⚠ Vulnerability found" if vuln else "✓ Clean"
                print(f"  Status: {status}")
            else:
                print(f"  ✗ Error: {result.get('error', 'Unknown')}")
            
            if i < len(files):
                time.sleep(DELAY_BETWEEN_FILES)
        
        return results
    
    def save_results(self, results, output_file=None):
        """Save results"""
        os.makedirs(OUTPUT_DIR, exist_ok=True)
        
        if output_file is None:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            output_file = os.path.join(OUTPUT_DIR, f'scan_results_claude_{timestamp}.json')
        
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(results, f, indent=2, ensure_ascii=False)
        
        print("\n" + "=" * 60)
        print("Scan complete!")
        print("=" * 60)
        print(f"Total: {len(results)} | Success: {self.success_count} | Failed: {self.fail_count}")
        print(f"Results saved to: {output_file}")
        
        vuln_count = sum(1 for r in results if r.get('success') and 
                        r.get('analysis', {}).get('has_vulnerability'))
        print(f"Vulnerabilities detected: {vuln_count}")
        
        total_tokens = sum(r.get('tokens_used', 0) for r in results if r.get('success'))
        if total_tokens > 0:
            print(f"Total tokens used: {total_tokens:,}")
        
        return output_file
