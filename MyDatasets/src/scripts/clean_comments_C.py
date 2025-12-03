#!/usr/bin/env python3
"""
Script to remove C/C++ style comments from files and rename them sequentially.
Removes /* */ and // comments while preserving all other code.
"""

import os
import re
import sys
from pathlib import Path


def remove_comments(code):
    """
    Remove C/C++ style comments (// and /* */) from code.
    Handles multi-line comments and avoids removing comment markers in strings.
    """
    
    def replacer(match):
        s = match.group(0)
        if s.startswith('/'):
            return " "  # Replace comment with space
        else:
            return s  # Keep string literals as-is
    
    # Pattern matches:
    # - C++ style comments: //.*?$
    # - C style comments: /\*.*?\*/
    # - Double-quoted strings: "(?:\\.|[^"\\])*"
    # - Single-quoted strings: '(?:\\.|[^'\\])*'
    pattern = re.compile(
        r'//.*?$|/\*.*?\*/|\'(?:\\.|[^\\\'])*\'|"(?:\\.|[^\\"])*"',
        re.DOTALL | re.MULTILINE
    )
    
    return re.sub(pattern, replacer, code)


def process_files(source_folder, output_folder=None):
    """
    Process all files in the source folder, remove comments, and rename sequentially.
    
    Args:
        source_folder: Path to the folder containing files to process
        output_folder: Path to output folder (if None, creates 'cleaned' subfolder)
    """
    
    source_path = Path(source_folder)
    
    if not source_path.exists():
        print(f"Error: Source folder '{source_folder}' does not exist!")
        return
    
    if not source_path.is_dir():
        print(f"Error: '{source_folder}' is not a directory!")
        return
    
    # Set output folder
    if output_folder is None:
        output_path = source_path / "cleaned"
    else:
        output_path = Path(output_folder)
    
    # Create output directory if it doesn't exist
    output_path.mkdir(parents=True, exist_ok=True)
    
    # Get all files (excluding directories)
    files = [f for f in source_path.iterdir() if f.is_file()]
    
    if not files:
        print(f"No files found in '{source_folder}'")
        return
    
    # Sort files for consistent ordering
    files.sort()
    
    # Determine padding width based on number of files
    num_files = len(files)
    padding_width = len(str(num_files))
    
    print(f"Found {num_files} file(s) to process")
    print(f"Output directory: {output_path}")
    print("-" * 60)
    
    # Process each file
    processed_count = 0
    for index, file_path in enumerate(files, start=1):
        try:
            # Read the original file
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
            
            # Remove comments
            cleaned_content = remove_comments(content)
            
            # Determine new filename
            original_ext = file_path.suffix
            if not original_ext:
                original_ext = '.txt'  # Default extension
            
            # Create new filename: vulnerable_clean_01.c, vulnerable_clean_02.c, etc.
            new_filename = f"vulnerable_clean_{str(index).zfill(padding_width)}{original_ext}"
            new_file_path = output_path / new_filename
            
            # Write cleaned content to new file
            with open(new_file_path, 'w', encoding='utf-8') as f:
                f.write(cleaned_content)
            
            print(f"✓ Processed: {file_path.name} → {new_filename}")
            processed_count += 1
            
        except Exception as e:
            print(f"✗ Error processing {file_path.name}: {str(e)}")
    
    print("-" * 60)
    print(f"Successfully processed {processed_count}/{num_files} file(s)")
    print(f"Cleaned files saved to: {output_path.absolute()}")


def main():
    """Main function to handle command-line arguments."""
    
    if len(sys.argv) < 2:
        print("Usage: python clean_comments.py <source_folder> [output_folder]")
        print("\nExample:")
        print("  python clean_comments.py ./my_code_files")
        print("  python clean_comments.py ./my_code_files ./cleaned_output")
        sys.exit(1)
    
    source_folder = sys.argv[1]
    output_folder = sys.argv[2] if len(sys.argv) > 2 else None
    
    process_files(source_folder, output_folder)


if __name__ == "__main__":
    main()