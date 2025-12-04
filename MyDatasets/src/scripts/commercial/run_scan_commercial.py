# run_scan_commercial.py
# Usage：Running scan with commercial LLMs (Claude, ChatGPT, Gemini)

import argparse
from scanner_commercial import CommercialVulnerabilityScanner
from config_commercial import SCAN_PATTERN, LLM_PROVIDER

def main():
    """Main function to run the commercial LLM vulnerability scanner"""
    parser = argparse.ArgumentParser(
        description='Using commercial LLMs (Claude/ChatGPT/Gemini) to scan C/C++ code for buffer overflow vulnerabilities in bulk'
    )
    parser.add_argument(
        'directory',
        help='Directory path to scan'
    )
    parser.add_argument(
        '-p', '--pattern',
        default=SCAN_PATTERN,
        help=f'File matching pattern (default: {SCAN_PATTERN})'
    )
    parser.add_argument(
        '-o', '--output',
        help='Output file path (default: auto-generated filename with timestamp)'
    )
    parser.add_argument(
        '-t', '--test',
        type=int,
        nargs='?',
        const=5,
        metavar='N',
        help='Test mode: scan only the first N files (default: 5)'
    )
    parser.add_argument(
        '-l', '--llm',
        choices=['claude', 'chatgpt', 'gemini'],
        default=LLM_PROVIDER,
        help=f'Select LLM provider (default: {LLM_PROVIDER})'
    )
    
    args = parser.parse_args()
    
    print("=" * 60)
    print(f"Commercial LLM Vulnerability Scanner - {args.llm.upper()}")
    print("=" * 60)
    print(f"Scan Directory: {args.directory}")
    print(f"File Pattern: {args.pattern}")
    
    if args.test:
        print(f"Test mode: scanning only the first {args.test} files")
    
    # Create scanner instance
    try:
        scanner = CommercialVulnerabilityScanner(provider=args.llm)
    except (ValueError, ImportError) as e:
        print(f"\nError: {e}")
        print("\nPlease check:")
        print("1. Whether the API key is set (config_commercial.py)")
        print("2. Whether the corresponding SDK is installed")
        print("   pip install anthropic openai google-generativeai")
        return
    
    # Scan directory
    try:
        results = scanner.scan_directory(args.directory, args.pattern, max_files=args.test)
        
        # Save results
        if results:
            scanner.save_results(results, args.output)
        else:
            print("\nNo files found or scan failed")
    except Exception as e:
        print(f"\nError during scanning: {e}")

if __name__ == "__main__":
    main()