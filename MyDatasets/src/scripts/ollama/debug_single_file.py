#!/usr/bin/env python
# debug_single_file.py
# 用于调试单个文件扫描问题

import sys
import traceback
from scanner import VulnerabilityScanner

def debug_scan(file_path):
    """调试单个文件的扫描过程"""
    print("=" * 60)
    print("调试单文件扫描")
    print("=" * 60)
    print(f"文件: {file_path}\n")
    
    scanner = VulnerabilityScanner()
    
    try:
        # 步骤1: 读取文件
        print("步骤1: 读取文件内容...")
        code = scanner.read_file(file_path)
        print(f"✓ 文件读取成功 ({len(code)} 字符)")
        print(f"前100个字符: {code[:100]}...\n")
        
        # 步骤2: 构建prompt
        print("步骤2: 构建prompt...")
        from config import VULNERABILITY_PROMPT
        prompt = VULNERABILITY_PROMPT.format(code_content=code[:500])  # 只用前500字符测试
        print(f"✓ Prompt构建成功 ({len(prompt)} 字符)\n")
        
        # 步骤3: 调用API
        print("步骤3: 调用Ollama API...")
        import requests
        from config import OLLAMA_API_URL, MODEL_NAME
        
        payload = {
            "model": MODEL_NAME,
            "prompt": prompt,
            "stream": False,
            "temperature": 0.1
        }
        
        response = requests.post(OLLAMA_API_URL, json=payload, timeout=60)
        print(f"✓ API响应状态码: {response.status_code}\n")
        
        # 步骤4: 解析响应
        print("步骤4: 解析响应...")
        result = response.json()
        print(f"响应keys: {result.keys()}")
        print(f"\n完整响应:")
        print(result)
        
        if 'response' in result:
            print(f"\n模型回复:")
            print(result['response'][:500])
        
    except Exception as e:
        print(f"\n✗ 错误发生!")
        print(f"错误类型: {type(e).__name__}")
        print(f"错误信息: {e}")
        print(f"\n完整堆栈:")
        traceback.print_exc()

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("用法: python debug_single_file.py <文件路径>")
        print("例如: python debug_single_file.py ../../dataset_01/bad_code_clean/CWE121_xxx.c")
        sys.exit(1)
    
    debug_scan(sys.argv[1])