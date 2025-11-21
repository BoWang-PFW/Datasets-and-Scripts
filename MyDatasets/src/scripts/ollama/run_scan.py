# run_scan.py
# usage: Batch scan C/C++ code for buffer overflow vulnerabilities using Ollama API

import argparse
from scanner import VulnerabilityScanner
from config import SCAN_PATTERN

def main():
    # set up argument parser
    parser = argparse.ArgumentParser(
        description='Batch scan code for vulnerabilities using Ollama API'
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
        help='Path to output file (default: auto-generated with timestamp)'
    )
    parser.add_argument(
        '-t', '--test',
        type=int,
        nargs='?',
        const=5,
        metavar='N',
        help='Test mode: only scan the first N files (default: 5)'
    )
    
    args = parser.parse_args()
    
    print("=" * 60)
    print("Ollama Vulnerability Scanner")
    print("=" * 60)
    print(f"Scanning directory: {args.directory}")
    print(f"File pattern: {args.pattern}")

    if args.test:
        print(f"Test mode: only scan the first {args.test} files")

    # Create scanner instance
    scanner = VulnerabilityScanner()

    # Scan (limit file count in test mode)
    results = scanner.scan_directory(args.directory, args.pattern, max_files=args.test)

    # Save results
    if results:
        scanner.save_results(results, args.output)
    else:
        print("\nNo files found or scan failed")

if __name__ == "__main__":
    main()