# run_scan_api.py
# Usage: Run vulnerability scanning using commercial LLM APIs (ChatGPT or Claude)

import argparse
import os
from config import SCAN_PATTERN

def main():
    parser = argparse.ArgumentParser(
        description='Scan code for vulnerabilities using commercial LLM APIs'
    )
    parser.add_argument('directory', help='Directory to scan')
    parser.add_argument('-p', '--pattern', default=SCAN_PATTERN,
                       help=f'File pattern (default: {SCAN_PATTERN})')
    parser.add_argument('-o', '--output', help='Output file path')
    parser.add_argument('-t', '--test', type=int, nargs='?', const=5,
                       help='Test mode: scan first N files (default: 5)')
    
    # API selection
    parser.add_argument('--api', choices=['openai', 'claude'], required=True,
                       help='Which API to use: openai or claude')
    parser.add_argument('--key', help='API key (or set OPENAI_API_KEY/ANTHROPIC_API_KEY env var)')
    parser.add_argument('--model', help='Model name (optional, uses defaults)')
    
    args = parser.parse_args()
    
    # Get API key
    if args.key:
        api_key = args.key
    elif args.api == 'openai':
        api_key = os.environ.get('OPENAI_API_KEY')
        if not api_key:
            print("Error: Set OPENAI_API_KEY environment variable or use --key")
            return
    else:  # claude
        api_key = os.environ.get('ANTHROPIC_API_KEY')
        if not api_key:
            print("Error: Set ANTHROPIC_API_KEY environment variable or use --key")
            return
    
    print("=" * 60)
    print(f"Vulnerability Scanner - {args.api.upper()} API")
    print("=" * 60)
    print(f"Scanning: {args.directory}")
    print(f"Pattern: {args.pattern}")
    if args.test:
        print(f"Test mode: first {args.test} files")
    
    # Create scanner based on API choice
    if args.api == 'openai':
        from scanner_openai import VulnerabilityScannerOpenAI
        model = args.model or "gpt-4o-mini"  # Fast and cheap
        scanner = VulnerabilityScannerOpenAI(api_key=api_key, model=model)
        print(f"Model: {model}")
    else:  # claude
        from scanner_claude import VulnerabilityScannerClaude
        model = args.model or "claude-3-5-haiku-20241022"  # Fast and cheap
        scanner = VulnerabilityScannerClaude(api_key=api_key, model=model)
        print(f"Model: {model}")
    
    # Scan
    try:
        results = scanner.scan_directory(args.directory, args.pattern, max_files=args.test)
        
        if results:
            scanner.save_results(results, args.output)
        else:
            print("\nNo files found or scan failed")
    
    except Exception as e:
        print(f"\nError: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
