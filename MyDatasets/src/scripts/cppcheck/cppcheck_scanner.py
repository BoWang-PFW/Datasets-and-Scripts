#!/usr/bin/env python3
"""
Code checker script for C/C++ codes using Cppcheck.
This script mainly focuses on security vulnerabilities while ignoring style issues.
"""

import subprocess
import os
import sys
import json
from datetime import datetime

def run_cppcheck(input_dir, output_dir, report_format='html'):
    """
    Run cppcheck on the specified directory.
    report_format: 'html', 'xml', and 'text'
    """
    
    # create output directory if it doesn't exist
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    # generate timestamped report filenames
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    xml_report = os.path.join(output_dir, f"cppcheck_report_{timestamp}.xml")
    html_report = os.path.join(output_dir, f"cppcheck_report_{timestamp}.html")
    text_report = os.path.join(output_dir, f"cppcheck_report_{timestamp}.txt")
    
    # Cppcheck command construction
    cppcheck_cmd = [
        'cppcheck',
        
        # activate specific checks
        '--enable=warning,performance,portability',

        # focus on security vulnerabilities
        '--check-level=exhaustive',

        # ignore system headers and include errors
        '--suppress=missingIncludeSystem',
        '--suppress=missingInclude',
        '--suppress=unmatchedSuppression',

        # ignore naming and variable-related issues
        '--suppress=variableScope',
        '--suppress=unusedVariable',
        '--suppress=unusedFunction',
        '--suppress=constParameter',
        '--suppress=constVariable',
        '--suppress=constParameterCallback',
        '--suppress=constParameterPointer',
        '--suppress=constParameterReference',
        '--suppress=variableHidingTypedef',

        # suppress style-related warnings
        '--suppress=*style*',

        # include inconclusive results (important for security checks)
        '--inconclusive',

        # force all configurations to be checked
        '--force',

        # show progress
        '--verbose',

        # XML output (for later HTML generation)
        '--xml',
        '--xml-version=2',

        # output file
        f'--output-file={xml_report}',

        # directory to scan
        input_dir
    ]

    print(f"Starting directory scan: {input_dir}")
    print(f"Executing command: {' '.join(cppcheck_cmd)}")
    print("-" * 80)

    # Run cppcheck
    try:
        result = subprocess.run(
            cppcheck_cmd,
            capture_output=True,
            text=True,
            timeout=3600  # timeout after 1 hour   
        )

        # Print stderr (cppcheck progress information is in stderr)
        if result.stderr:
            print("Scan output:")
            print(result.stderr)
        
        print("-" * 80)
        print(f"Scan completed! XML report saved to: {xml_report}")

    except subprocess.TimeoutExpired:
        print("Error: Scan timed out (exceeded 1 hour)")
        return None
    except FileNotFoundError:
        print("Error: cppcheck command not found. Please ensure cppcheck is installed.")
        return None
    except Exception as e:
        print(f"Error: {e}")
        return None

    # Generate HTML report
    if report_format == 'html' or report_format == 'both':
        print("\nGenerating HTML report...")
        generate_html_report(xml_report, html_report)

    # Generate text summary
    print("\nGenerating text summary...")
    generate_text_summary(xml_report, text_report)
    
    return {
        'xml': xml_report,
        'html': html_report,
        'text': text_report
    }

def generate_html_report(xml_file, html_file):
    """
    Generate HTML report using cppcheck-htmlreport
    """
    try:
        cmd = [
            'cppcheck-htmlreport',
            f'--file={xml_file}',
            f'--report-dir={os.path.dirname(html_file)}',
            '--source-dir=.'
        ]
        
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.returncode == 0:
            print(f"HTML report generated: {os.path.dirname(html_file)}/index.html")
        else:
            print(f"HTML report generation failed: {result.stderr}")

    except FileNotFoundError:
        print("Warning: cppcheck-htmlreport not found. Skipping HTML report generation.")
        print("You can install it using the following command: pip install cppcheck-htmlreport")
    except Exception as e:
        print(f"HTML report generation error: {e}")

def generate_text_summary(xml_file, text_file):
    """
    Generate text summary from XML file
    """
    import xml.etree.ElementTree as ET
    
    try:
        tree = ET.parse(xml_file)
        root = tree.getroot()

        # Statistics
        errors = root.findall('.//error')

        # Categorize by severity
        severity_count = {}
        issues_by_severity = {}
        
        for error in errors:
            severity = error.get('severity', 'unknown')
            msg = error.get('msg', '')
            file_location = error.find('location')

            # Statistics
            severity_count[severity] = severity_count.get(severity, 0) + 1

            # Collect detailed information
            if severity not in issues_by_severity:
                issues_by_severity[severity] = []
            
            issue_info = {
                'msg': msg,
                'id': error.get('id', ''),
                'file': file_location.get('file', '') if file_location is not None else '',
                'line': file_location.get('line', '') if file_location is not None else ''
            }
            issues_by_severity[severity].append(issue_info)

        # Write text report
        with open(text_file, 'w', encoding='utf-8') as f:
            f.write("=" * 80 + "\n")
            f.write("Cppcheck Security Vulnerability Scan Report\n")
            f.write(f"Generated Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write("=" * 80 + "\n\n")

            # Overall Statistics
            f.write("Overall Statistics:\n")
            f.write("-" * 80 + "\n")
            f.write(f"Total Issues: {len(errors)}\n\n")

            for severity in sorted(severity_count.keys()):
                f.write(f"  {severity.upper()}: {severity_count[severity]}\n")
            
            f.write("\n" + "=" * 80 + "\n\n")

            # Categorize by severity
            priority_order = ['error', 'warning', 'performance', 'portability', 'information']
            
            for severity in priority_order:
                if severity not in issues_by_severity:
                    continue

                f.write(f"\n{severity.upper()} ({len(issues_by_severity[severity])} issues):\n")
                f.write("-" * 80 + "\n")
                
                for idx, issue in enumerate(issues_by_severity[severity], 1):
                    f.write(f"\n[{idx}] {issue['id']}\n")
                    f.write(f"    File: {issue['file']}\n")
                    f.write(f"    Line: {issue['line']}\n")
                    f.write(f"    Description: {issue['msg']}\n")

            # Add other severities not in priority order
            for severity in issues_by_severity:
                if severity not in priority_order:
                    f.write(f"\n{severity.upper()} ({len(issues_by_severity[severity])} issues):\n")
                    f.write("-" * 80 + "\n")
                    
                    for idx, issue in enumerate(issues_by_severity[severity], 1):
                        f.write(f"\n[{idx}] {issue['id']}\n")
                        f.write(f"    File: {issue['file']}\n")
                        f.write(f"    Line: {issue['line']}\n")
                        f.write(f"    Description: {issue['msg']}\n")

        print(f"Text summary has been saved to: {text_file}")

        # Print summary to console
        print("\n" + "=" * 80)
        print("Scan Results Summary:")
        print("-" * 80)
        print(f"Total Issues: {len(errors)}")
        for severity in sorted(severity_count.keys()):
            print(f"  {severity.upper()}: {severity_count[severity]}")
        print("=" * 80)
        
    except Exception as e:
        print(f"Error occurred while generating text summary: {e}")

def scan_single_file(file_path, output_dir):
    """
    Scan a single file
    """
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_file = os.path.join(output_dir, f"single_file_report_{timestamp}.txt")
    
    cppcheck_cmd = [
        'cppcheck',
        '--enable=warning,performance,portability',
        '--check-level=exhaustive',
        '--suppress=missingIncludeSystem',
        '--suppress=missingInclude',
        '--suppress=*style*',
        '--inconclusive',
        '--template={file}:{line}: [{severity}] {id}: {message}',
        file_path
    ]

    print(f"Scanning file: {file_path}")

    try:
        result = subprocess.run(
            cppcheck_cmd,
            capture_output=True,
            text=True,
            timeout=300
        )
        
        # Write output to file
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(f"File: {file_path}\n")
            f.write(f"Scan Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write("=" * 80 + "\n\n")
            f.write(result.stderr)
        
        print(result.stderr)
        print(f"\nReport has been saved to: {output_file}")
        
    except Exception as e:
        print(f"Error occurred: {e}")

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage:")
        print("  Scan Directory: python script.py <input_dir> <output_dir> [html|text|both]")
        print("  Scan Single File: python script.py --file <file_path> <output_dir>")
        print("\nExamples:")
        print("  python script.py ./bad_dataset ./reports html")
        print("  python script.py --file test.c ./reports")
        sys.exit(1)
    
    if sys.argv[1] == '--file':
        # Scan a single file
        if len(sys.argv) < 4:
            print("Error occurred: Please provide file path and output directory")
            sys.exit(1)
        scan_single_file(sys.argv[2], sys.argv[3])
    else:
        # Scan Directory
        input_dir = sys.argv[1]
        output_dir = sys.argv[2]
        report_format = sys.argv[3] if len(sys.argv) > 3 else 'both'
        
        if not os.path.exists(input_dir):
            print(f"Error occurred: Input directory does not exist: {input_dir}")
            sys.exit(1)
        
        reports = run_cppcheck(input_dir, output_dir, report_format)
        
        if reports:
            print("\n" + "=" * 80)
            print("All Report Files:")
            print(f"  XML Report: {reports['xml']}")
            print(f"  HTML Report: {os.path.dirname(reports['html'])}/index.html")
            print(f"  Text Summary: {reports['text']}")
            print("=" * 80)