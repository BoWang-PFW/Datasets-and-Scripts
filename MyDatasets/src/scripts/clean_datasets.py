#!/usr/bin/env python3
"""
codeset clean script
usage: python CleanDataset.py <input_dir> <output_dir> <dataset_type>
dataset_type: 'good' or 'bad'
This script processes C/C++ source files to create 'good' or 'bad' datasets by removing specific
code blocks based on preprocessor directives and comments.
"""

import re
import os
import sys

def remove_comments(code):
    """remove C/C++ comments from code"""
    # Remove multi-line comments /* */
    code = re.sub(r'/\*.*?\*/', '', code, flags=re.DOTALL)
    # Remove single-line comments //
    code = re.sub(r'//.*?$', '', code, flags=re.MULTILINE)
    return code

def parse_preprocessor_blocks(lines):
    """
    Parse preprocessor directives and build a nested structure.
    Return a list of blocks, each containing:
    - type: 'code', 'ifndef', 'ifdef'
    - condition: for 'ifndef'/'ifdef' blocks
    - content: nested list of lines/blocks
    - start_line, end_line: line numbers in the original file
    """
    blocks = []
    i = 0
    
    while i < len(lines):
        line = lines[i].strip()
        
        # detect #ifndef
        ifndef_match = re.match(r'#ifndef\s+(\w+)', line)
        if ifndef_match:
            condition = ifndef_match.group(1)
            block_lines, end_idx = extract_block(lines, i)
            blocks.append({
                'type': 'ifndef',
                'condition': condition,
                'content': parse_preprocessor_blocks(block_lines),
                'start_line': i,
                'end_line': end_idx
            })
            i = end_idx + 1
            continue
        
        # detect #ifdef
        ifdef_match = re.match(r'#ifdef\s+(\w+)', line)
        if ifdef_match:
            condition = ifdef_match.group(1)
            block_lines, end_idx = extract_block(lines, i)
            blocks.append({
                'type': 'ifdef',
                'condition': condition,
                'content': parse_preprocessor_blocks(block_lines),
                'start_line': i,
                'end_line': end_idx
            })
            i = end_idx + 1
            continue

        # common code line
        blocks.append({
            'type': 'code',
            'content': lines[i],
            'start_line': i,
            'end_line': i
        })
        i += 1
    
    return blocks

def extract_block(lines, start_idx):
    """
    Extract all lines from start_idx to the matching #endif (excluding #ifndef/#ifdef and #endif).
    Return the lines within the block and the index of #endif.
    """
    depth = 0
    i = start_idx
    
    while i < len(lines):
        line = lines[i].strip()
        
        if re.match(r'#ifndef|#ifdef', line):
            depth += 1
        elif re.match(r'#endif', line):
            depth -= 1
            if depth == 0:
                # Found matching #endif
                return lines[start_idx + 1:i], i
        
        i += 1

    # If no matching #endif is found, return all remaining lines
    return lines[start_idx + 1:], len(lines) - 1

def filter_blocks(blocks, dataset_type):
    """
    Filter blocks based on dataset type
    dataset_type: 'good' or 'bad'
    """
    result = []
    
    for block in blocks:
        if block['type'] == 'code':
            result.append(block['content'])
        
        elif block['type'] == 'ifndef':
            condition = block['condition']
            
            if dataset_type == 'bad':
                # bad dataset: remove OMITGOOD blocks, keep OMITBAD block content
                if condition == 'OMITGOOD':
                    continue  # skip entire block
                elif condition == 'OMITBAD':
                    # keep content but omit #ifndef and #endif
                    result.extend(filter_blocks(block['content'], dataset_type))
                elif condition in ['_WIN32', '_WIN64']:
                    # remove platform-specific condition compilation
                    continue
                else:
                    # other conditions, keep but omit the markers
                    result.extend(filter_blocks(block['content'], dataset_type))
            
            elif dataset_type == 'good':
                # good dataset: remove OMITBAD blocks, keep OMITGOOD block content
                if condition == 'OMITBAD':
                    continue  # skip entire block
                elif condition == 'OMITGOOD':
                    # keep content but omit #ifndef and #endif
                    result.extend(filter_blocks(block['content'], dataset_type))
                elif condition in ['_WIN32', '_WIN64']:
                    # remove platform-specific condition compilation
                    continue
                else:
                    # other conditions, keep but omit the markers
                    result.extend(filter_blocks(block['content'], dataset_type))
        
        elif block['type'] == 'ifdef':
            condition = block['condition']
            
            # For #ifdef INCLUDEMAIN, need to recursively process internal OMITGOOD/OMITBAD
            if condition == 'INCLUDEMAIN':
                result.extend(filter_blocks(block['content'], dataset_type))
            else:
                # Other #ifdef blocks remove markers but keep content
                result.extend(filter_blocks(block['content'], dataset_type))
    
    return result

def process_file(input_path, output_path, dataset_type):
    """
    Process a single file
    dataset_type: 'good' or 'bad'
    """
    with open(input_path, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()
    
    # step 1: remove comments
    content = remove_comments(content)

    # step 2: split into lines
    lines = content.split('\n')

    # step 3: parse preprocessor blocks
    blocks = parse_preprocessor_blocks(lines)
    
    # step 4: filter blocks based on dataset type
    filtered_lines = filter_blocks(blocks, dataset_type)
    
    # step 5: join lines back
    result = '\n'.join(filtered_lines)

    # clean up excessive blank lines (keep at most 2 consecutive blank lines)
    result = re.sub(r'\n{3,}', '\n\n', result)

    # write to output file
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(result)

def process_directory(input_dir, output_dir, dataset_type):
    """
    Process an entire directory of files
    dataset_type: 'good' or 'bad'
    """
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    for root, dirs, files in os.walk(input_dir):
        for file in files:
            if file.endswith(('.c', '.cpp', '.h', '.hpp')):
                input_path = os.path.join(root, file)
                rel_path = os.path.relpath(input_path, input_dir)
                output_path = os.path.join(output_dir, rel_path)
                
                # create output directory if not exists
                os.makedirs(os.path.dirname(output_path), exist_ok=True)
                
                print(f"Processing: {rel_path}")
                try:
                    process_file(input_path, output_path, dataset_type)
                except Exception as e:
                    print(f"Error processing {rel_path}: {e}")

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: python script.py <input_dir> <output_dir> <dataset_type>")
        print("dataset_type: 'good' or 'bad'")
        sys.exit(1)
    
    input_dir = sys.argv[1]
    output_dir = sys.argv[2]
    dataset_type = sys.argv[3].lower()
    
    if dataset_type not in ['good', 'bad']:
        print("Error: dataset_type must be 'good' or 'bad'")
        sys.exit(1)
    
    process_directory(input_dir, output_dir, dataset_type)
    print("Processing complete!")