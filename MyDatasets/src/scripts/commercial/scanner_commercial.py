# scanner_commercial.py
# Usage：Support Claude, ChatGPT, Gemini commercial LLM scanners

import json
import os
from pathlib import Path
from datetime import datetime
import time
import re
from config_commercial import (
    LLM_PROVIDER, CLAUDE_API_KEY, CHATGPT_API_KEY, GEMINI_API_KEY,
    MODEL_CONFIGS, VULNERABILITY_PROMPT, DELAY_BETWEEN_FILES,
    REQUEST_TIMEOUT, OUTPUT_DIR
)

# Import the respective SDKs for each LLM
try:
    import anthropic
    CLAUDE_AVAILABLE = True
except ImportError:
    CLAUDE_AVAILABLE = False

try:
    import openai
    CHATGPT_AVAILABLE = True
except ImportError:
    CHATGPT_AVAILABLE = False

try:
    import google.generativeai as genai
    GEMINI_AVAILABLE = True
except ImportError:
    GEMINI_AVAILABLE = False


class LLMClient:
    """Base class for LLM clients"""
    
    def __init__(self, provider):
        self.provider = provider
        self.config = MODEL_CONFIGS.get(provider, {})
        self.model_name = self.config.get("model_name")
    
    def analyze(self, prompt):
        """Analyze code and return LLM response"""
        raise NotImplementedError


class ClaudeClient(LLMClient):
    """Claude API client"""
    
    def __init__(self):
        super().__init__("claude")
        if not CLAUDE_API_KEY:
            raise ValueError("CLAUDE_API_KEY not set")
        self.client = anthropic.Anthropic(api_key=CLAUDE_API_KEY)
    
    def analyze(self, prompt):
        response = self.client.messages.create(
            model=self.model_name,
            max_tokens=self.config["max_tokens"],
            temperature=self.config["temperature"],
            messages=[
                {"role": "user", "content": prompt}
            ]
        )
        return response.content[0].text


class ChatGPTClient(LLMClient):
    """ChatGPT API client"""
    
    def __init__(self):
        super().__init__("chatgpt")
        if not CHATGPT_API_KEY:
            raise ValueError("CHATGPT_API_KEY not set")
        self.client = openai.OpenAI(api_key=CHATGPT_API_KEY)
    
    def analyze(self, prompt):
        response = self.client.chat.completions.create(
            model=self.model_name,
            messages=[
                {"role": "user", "content": prompt}
            ],
            temperature=self.config["temperature"],
            max_tokens=self.config["max_tokens"]
        )
        return response.choices[0].message.content


class GeminiClient(LLMClient):
    """Gemini API client"""
    
    def __init__(self):
        super().__init__("gemini")
        if not GEMINI_API_KEY:
            raise ValueError("GEMINI_API_KEY not set")
        genai.configure(api_key=GEMINI_API_KEY)
        self.model = genai.GenerativeModel(self.model_name)
    
    def analyze(self, prompt):
        response = self.model.generate_content(
            prompt,
            generation_config={
                "temperature": self.config["temperature"],
                "max_output_tokens": self.config["max_tokens"]
            }
        )
        return response.text


def create_llm_client(provider):
    """Create LLM client"""
    clients = {
        "claude": (ClaudeClient, CLAUDE_AVAILABLE),
        "chatgpt": (ChatGPTClient, CHATGPT_AVAILABLE),
        "gemini": (GeminiClient, GEMINI_AVAILABLE)
    }
    
    if provider not in clients:
        raise ValueError(f"Unsupported LLM: {provider}")
    
    client_class, available = clients[provider]
    
    if not available:
        raise ImportError(f"{provider} SDK not installed, please run: pip install {provider}")
    
    return client_class()


class CommercialVulnerabilityScanner:
    """Commercial LLM vulnerability scanner"""
    
    def __init__(self, provider=None):
        self.provider = provider or LLM_PROVIDER
        self.llm_client = create_llm_client(self.provider)
        self.scan_count = 0
        self.success_count = 0
        self.fail_count = 0
        
        print(f"Using LLM: {self.provider}")
        print(f"Model: {self.llm_client.model_name}")
    
    def read_file(self, file_path):
        """Read file content with multiple encodings"""
        encodings = ['utf-8', 'gbk', 'gb2312', 'latin-1']
        
        for encoding in encodings:
            try:
                with open(file_path, 'r', encoding=encoding) as f:
                    return f.read()
            except UnicodeDecodeError:
                continue
            except Exception as e:
                raise Exception(f"Failed to read file: {e}")
        
        raise Exception("Failed to read file with common encodings")
    
    def parse_llm_response(self, response_text):
        """Parse JSON result returned by LLM"""
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
            'raw_response': response_text[:500],
            'note': 'Failed to parse JSON, used keyword detection'
        }
    
    def scan_single_file(self, file_path):
        """Scan a single file"""
        self.scan_count += 1
        
        result = {
            'file': str(file_path),
            'file_name': Path(file_path).name,
            'scan_number': self.scan_count,
            'llm_provider': self.provider,
            'model_name': self.llm_client.model_name,
            'timestamp': datetime.now().isoformat(),
            'success': False
        }
        
        try:
            # Read code content
            code_content = self.read_file(file_path)
            result['file_size'] = len(code_content)
            result['line_count'] = code_content.count('\n') + 1
            
            # Build prompt
            prompt = VULNERABILITY_PROMPT.format(code_content=code_content)
            
            # Call LLM
            model_response = self.llm_client.analyze(prompt)
            
            # Parse response
            parsed_result = self.parse_llm_response(model_response)
            
            result.update({
                'success': True,
                'model_response': model_response,
                'analysis': parsed_result
            })
            
            self.success_count += 1
            
        except Exception as e:
            result['error'] = str(e)
            self.fail_count += 1
        
        return result
    
    def scan_directory(self, directory, pattern='*.c', max_files=None):
        """Scan all matching files in a directory"""
        directory_path = Path(directory)
        if not directory_path.exists():
            raise FileNotFoundError(f"Directory does not exist: {directory}")
        
        all_files = list(directory_path.rglob(pattern))
        
        if not all_files:
            print(f"Warning: No {pattern} files found in {directory}")
            return []
        
        # If max_files is set, only scan the first N files
        if max_files and max_files < len(all_files):
            files = all_files[:max_files]
            print(f"\nFound {len(all_files)} files, scanning first {max_files} in test mode")
        else:
            files = all_files
            print(f"\nFound {len(files)} files to scan")
        
        print("=" * 60)
        
        results = []
        
        for i, file_path in enumerate(files, 1):
            print(f"\n[{i}/{len(files)}] Scanning: {file_path.name}")
            print(f"  Path: {file_path}")
            
            # Scan single file
            result = self.scan_single_file(file_path)
            results.append(result)
            
            # Display results
            if result['success']:
                analysis = result['analysis']
                has_vuln = analysis.get('has_vulnerability', False)
                status = "Vulnerability found" if has_vuln else " No vulnerability found"
                print(f"  Status: {status}")
                
                if has_vuln and 'description' in analysis:
                    print(f"  Description: {analysis['description'][:80]}")
            else:
                print(f"  Error: {result.get('error', 'Unknown error')}")
            
            # Delay between files
            if i < len(files):
                time.sleep(DELAY_BETWEEN_FILES)
        
        return results
    
    def save_results(self, results, output_file=None):
        """Save scan results to a JSON file"""
        os.makedirs(OUTPUT_DIR, exist_ok=True)
        
        if output_file is None:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            output_file = os.path.join(OUTPUT_DIR, f'scan_{self.provider}_{timestamp}.json')
        
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(results, f, indent=2, ensure_ascii=False)
        
        print("\n" + "=" * 60)
        print("Scan completed!")
        print("=" * 60)
        print(f"LLM: {self.provider} ({self.llm_client.model_name})")
        print(f"Total files: {len(results)}")
        print(f"Successes: {self.success_count}")
        print(f"Failures: {self.fail_count}")
        print(f"Results saved to: {output_file}")
        
        vuln_count = sum(1 for r in results 
                        if r.get('success') and 
                        r.get('analysis', {}).get('has_vulnerability', False))
        print(f"Files with vulnerabilities detected: {vuln_count}")
        
        return output_file