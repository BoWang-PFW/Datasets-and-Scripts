#!/usr/bin/env python3
"""
Vulnerability Scan Results Analyzer
Supports statistical analysis and CSV export
"""

import json
import csv
import argparse
from pathlib import Path
from collections import Counter
from datetime import datetime


class ResultAnalyzer:
    """Result Analyzer"""
    
    def __init__(self, result_file):
        self.result_file = result_file
        with open(result_file, 'r', encoding='utf-8') as f:
            self.results = json.load(f)
        self.stats = self._analyze()
    
    def _analyze(self):
        """Analyze results and generate statistics"""
        total = len(self.results)
        success = [r for r in self.results if r.get('success')]
        
        # Classification
        vulnerabilities = []
        safe_files = []
        parsed = 0
        
        for r in success:
            analysis = r.get('analysis', {})
            if analysis.get('parsed'):
                parsed += 1
                if analysis.get('has_vulnerability'):
                    vulnerabilities.append(r)
                else:
                    safe_files.append(r)
        
        return {
            'total': total,
            'success_count': len(success),
            'failed_count': total - len(success),
            'parsed_count': parsed,
            'vulnerabilities': vulnerabilities,
            'safe_files': safe_files,
            'vuln_types': Counter(
                v.get('analysis', {}).get('vulnerability_type', 'unknown') 
                for v in vulnerabilities
            ),
            'severities': Counter(
                v.get('analysis', {}).get('severity', 'unknown') 
                for v in vulnerabilities
            )
        }
    
    def print_summary(self):
        """Print statistical summary"""
        s = self.stats
        print("\n" + "="*70)
        print("Vulnerability Scan Results Analysis Summary")
        print("="*70)
        
        print(f"\n Overall Statistics:")
        print(f"  Total files: {s['total']}")
        print(f"  Successful scans: {s['success_count']} ({s['success_count']/s['total']*100:.1f}%)")
        print(f"  Failed scans: {s['failed_count']}")
        print(f"  Successfully parsed JSON: {s['parsed_count']}/{s['success_count']} "
              f"({s['parsed_count']/s['success_count']*100:.1f}%)" if s['success_count'] > 0 else "")
        
        vuln_count = len(s['vulnerabilities'])
        safe_count = len(s['safe_files'])
        
        print(f"\n🔍 Scan Results:")
        if s['success_count'] > 0:
            print(f"  Vulnerabilities found: {vuln_count} ({vuln_count/s['success_count']*100:.1f}%)")
            print(f"  Safe files: {safe_count} ({safe_count/s['success_count']*100:.1f}%)")
        
        if s['vuln_types']:
            print(f"\n Vulnerability Types:")
            for vtype, count in s['vuln_types'].most_common():
                print(f"  • {vtype}: {count}")
        
        if s['severities']:
            print(f"\n⚡ Severity Levels:")
            severity_emoji = {'high': '🔴', 'medium': '🟡', 'low': '🟢', 
                            'none': '⚪', 'unknown': '⚫'}
            severity_order = {'high': 3, 'medium': 2, 'low': 1, 'none': 0, 'unknown': -1}
            sorted_severities = sorted(s['severities'].items(), 
                                      key=lambda x: severity_order.get(x[0], -2), 
                                      reverse=True)
            for severity, count in sorted_severities:
                emoji = severity_emoji.get(severity, '•')
                print(f"  {emoji} {severity}: {count}")
    
    def print_vulnerabilities(self, limit=10, verbose=False):
        """Print vulnerability details"""
        vulns = self.stats['vulnerabilities']
        if not vulns:
            print("\nNo vulnerabilities found!")
            return
        
        print(f"\n{'='*70}")
        print(f"Vulnerability Details (showing {min(limit, len(vulns))} / {len(vulns)})")
        print("="*70)
        
        for i, v in enumerate(vulns[:limit], 1):
            analysis = v.get('analysis', {})
            print(f"\n[{i}] {v['file_name']}")
            print(f"    {v['file']}")
            print(f"    Type: {analysis.get('vulnerability_type', 'unknown')}")
            print(f"    Severity: {analysis.get('severity', 'unknown')}")
            
            if analysis.get('line_numbers'):
                print(f"    Line numbers: {', '.join(map(str, analysis['line_numbers']))}")
            
            desc = analysis.get('description', '')
            if desc:
                desc = desc if verbose or len(desc) <= 150 else desc[:150] + "..."
                print(f"    {desc}")
            
            if analysis.get('confidence'):
                print(f"    Confidence: {analysis['confidence']}%")
            
            if verbose:
                fix = analysis.get('secure_fix') or analysis.get('secure_implementation')
                if fix:
                    print(f"    Fix Suggestions:")
                    for line in fix.split('\n')[:8]:
                        if line.strip():
                            print(f"       {line}")
    
    def export_csv(self, output_file, include_all=True):
        """
        Export results to CSV
        
        Args:
            output_file: Path to the output CSV file
            include_all: Whether to include all fields (True) or only basic fields (False)
        """
        all_files = self.stats['vulnerabilities'] + self.stats['safe_files']
        
        # Basic fields
        basic_headers = [
            'File Name', 'File Path', 'Has Vulnerability', 'Vulnerability Type', 
            'Severity', 'Line Numbers', 'Confidence', 'JSON Parsed Successfully'
        ]
        
        # Full fields
        full_headers = basic_headers + ['Description', 'Fix Suggestions']
        
        headers = full_headers if include_all else basic_headers
        
        with open(output_file, 'w', newline='', encoding='utf-8-sig') as f:
            writer = csv.writer(f)
            writer.writerow(headers)
            
            for result in all_files:
                analysis = result.get('analysis', {})
                
                row = [
                    result.get('file_name', ''),
                    result.get('file', ''),
                    'Yes' if analysis.get('has_vulnerability') else 'No',
                    analysis.get('vulnerability_type', 'N/A'),
                    analysis.get('severity', 'N/A'),
                    ', '.join(map(str, analysis.get('line_numbers', []))),
                    analysis.get('confidence', 0),
                    'Yes' if analysis.get('parsed') else 'No'
                ]
                
                if include_all:
                    row.extend([
                        analysis.get('description', '')[:500],  # Limit description length
                        (analysis.get('secure_fix') or 
                         analysis.get('secure_implementation', ''))[:500]
                    ])
                
                writer.writerow(row)
        
        print(f"\nCSV exported to: {output_file}")
        print(f"   Contains {len(all_files)} records")
    
    def export_vulnerability_only_csv(self, output_file):
        """Export only files with vulnerabilities to CSV"""
        vulns = self.stats['vulnerabilities']
        
        if not vulns:
            print("\n No vulnerabilities found, no export needed")
            return
        
        headers = [
            'Index', 'File Name', 'File Path', 'Vulnerability Type', 'Severity',
            'Line Numbers', 'Confidence', 'Description', 'Fix Suggestions'
        ]
        
        with open(output_file, 'w', newline='', encoding='utf-8-sig') as f:
            writer = csv.writer(f)
            writer.writerow(headers)
            
            for i, v in enumerate(vulns, 1):
                analysis = v.get('analysis', {})
                writer.writerow([
                    i,
                    v.get('file_name', ''),
                    v.get('file', ''),
                    analysis.get('vulnerability_type', 'unknown'),
                    analysis.get('severity', 'unknown'),
                    ', '.join(map(str, analysis.get('line_numbers', []))),
                    analysis.get('confidence', 0),
                    analysis.get('description', '')[:500],
                    (analysis.get('secure_fix') or 
                     analysis.get('secure_implementation', ''))[:500]
                ])
        
        print(f"\n Vulnerability CSV exported to: {output_file}")
        print(f"   Contains {len(vulns)} vulnerabilities")


def main():
    parser = argparse.ArgumentParser(
        description='Analyze vulnerability scan results and export to CSV',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Basic analysis
  python analyze_results_simplified.py results.json
  
  # Export all results to CSV
  python analyze_results_simplified.py results.json -c all_results.csv
  
  # Export only vulnerabilities to CSV
  python analyze_results_simplified.py results.json -v vuln_only.csv
  
  # Show detailed information and export
  python analyze_results_simplified.py results.json --verbose -c results.csv
        """
    )
    
    parser.add_argument('result_file', help='Scan result JSON file')
    parser.add_argument('-c', '--csv', help='Export all results to CSV file')
    parser.add_argument('-v', '--vuln-csv', help='Export only vulnerabilities to CSV file')
    parser.add_argument('-l', '--limit', type=int, default=10,
                       help='Limit number of vulnerabilities displayed (default: 10)')
    parser.add_argument('--all', action='store_true',
                       help='Show all vulnerabilities instead of limiting the number')
    parser.add_argument('--verbose', action='store_true',
                       help='Show detailed information including fix suggestions')
    parser.add_argument('--basic-csv', action='store_true',
                       help='CSV contains only basic fields (excluding description and fix suggestions)')
    
    args = parser.parse_args()
    
    # Check if file exists
    if not Path(args.result_file).exists():
        print(f"Error: File does not exist {args.result_file}")
        return
    
    # Analyze results
    print(f"Loading results: {args.result_file}")
    analyzer = ResultAnalyzer(args.result_file)
    
    # Print summary
    analyzer.print_summary()
    
    # Print vulnerability details
    limit = len(analyzer.stats['vulnerabilities']) if args.all else args.limit
    analyzer.print_vulnerabilities(limit, args.verbose)
    
    # Export CSV
    if args.csv:
        analyzer.export_csv(args.csv, include_all=not args.basic_csv)
    
    if args.vuln_csv:
        analyzer.export_vulnerability_only_csv(args.vuln_csv)
    
    print("\n" + "="*70 + "\n")


if __name__ == "__main__":
    main()