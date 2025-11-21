# analyze_results.py
# usage: Analyze and summarize results from Ollama-based C/C++ vulnerability scanner

import json
import argparse
from pathlib import Path
from collections import Counter

def load_results(result_file):
    # load JSON results from file
    with open(result_file, 'r', encoding='utf-8') as f:
        return json.load(f)

def analyze_results(results):
    # analyze scan results
    total = len(results)
    success = sum(1 for r in results if r.get('success'))
    failed = total - success

    # count vulnerabilities
    vulnerabilities = []
    no_vulnerabilities = []
    
    for result in results:
        if result.get('success'):
            analysis = result.get('analysis', {})
            if analysis.get('has_vulnerability'):
                vulnerabilities.append(result)
            else:
                no_vulnerabilities.append(result)

    # count severity
    severity_counter = Counter()
    for vuln in vulnerabilities:
        severity = vuln.get('analysis', {}).get('severity', 'unknown')
        severity_counter[severity] += 1
    
    return {
        'total': total,
        'success': success,
        'failed': failed,
        'vulnerabilities': vulnerabilities,
        'no_vulnerabilities': no_vulnerabilities,
        'severity_stats': dict(severity_counter)
    }

def print_summary(stats):
    # print summary statistics
    print("\n" + "=" * 60)
    print("Scan Results Summary")
    print("=" * 60)

    print(f"\nTotal files scanned: {stats['total']}")
    print(f"Successfully scanned: {stats['success']} ({stats['success']/stats['total']*100:.1f}%)")
    print(f"Scan failed: {stats['failed']}")

    vuln_count = len(stats['vulnerabilities'])
    safe_count = len(stats['no_vulnerabilities'])

    print(f"\nVulnerabilities found: {vuln_count} ({vuln_count/stats['success']*100:.1f}%)")
    print(f"No vulnerabilities found: {safe_count} ({safe_count/stats['success']*100:.1f}%)")
    
    if stats['severity_stats']:
        print("\nSeverity distribution:")
        for severity, count in stats['severity_stats'].items():
            print(f"  {severity}: {count}")

def print_vulnerability_list(vulnerabilities, limit=10):
    # print vulnerability file list
    if not vulnerabilities:
        print("\nNo vulnerabilities found")
        return

    print(f"\nVulnerabilities found in files (showing top {min(limit, len(vulnerabilities))}):")
    print("-" * 60)
    
    for i, vuln in enumerate(vulnerabilities[:limit], 1):
        analysis = vuln.get('analysis', {})
        print(f"\n{i}. {vuln['file_name']}")
        print(f"   Path: {vuln['file']}")
        print(f"   Severity: {analysis.get('severity', 'unknown')}")

        if 'description' in analysis:
            desc = analysis['description'][:100]
            print(f"   Description: {desc}...")
        
        if analysis.get('line_numbers'):
            lines = analysis['line_numbers']
            print(f"   Line numbers: {lines}")

def compare_with_cppcheck(ollama_results_file, cppcheck_results_file):
    # compare Ollama results with cppcheck results
    print("\nComparison feature not implemented...")
    print("Hint: You can add logic to compare with cppcheck results here.")

def export_csv(stats, output_file):
    # export simple statistics in CSV format
    import csv
    
    with open(output_file, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['File Name', 'Path', 'Has Vulnerability', 'Severity', 'Description'])
        
        all_files = stats['vulnerabilities'] + stats['no_vulnerabilities']
        for result in all_files:
            analysis = result.get('analysis', {})
            writer.writerow([
                result['file_name'],
                result['file'],
                'Yes' if analysis.get('has_vulnerability') else 'No',
                analysis.get('severity', 'N/A'),
                analysis.get('description', '')[:100]
            ])

    print(f"\nCSV exported to: {output_file}")

def main():
    parser = argparse.ArgumentParser(description='Analyze vulnerability scan results')
    parser.add_argument('result_file', help='Scan results JSON file path')
    parser.add_argument('-l', '--limit', type=int, default=10,
                       help='Limit the number of vulnerability files displayed')
    parser.add_argument('-c', '--csv', help='Path to export CSV file')
    parser.add_argument('--all', action='store_true',
                       help='Show all vulnerability files (ignore limit)')
    
    args = parser.parse_args()

    # Load results
    results = load_results(args.result_file)

    # Analyze results
    stats = analyze_results(results)

    # Print summary
    print_summary(stats)

    # Print vulnerability list
    limit = None if args.all else args.limit
    if limit is None:
        limit = len(stats['vulnerabilities'])
    print_vulnerability_list(stats['vulnerabilities'], limit)

    # Export CSV
    if args.csv:
        export_csv(stats, args.csv)
    
    print("\n" + "=" * 60)

if __name__ == "__main__":
    main()