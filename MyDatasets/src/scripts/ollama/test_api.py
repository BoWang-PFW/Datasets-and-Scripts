# test_api.py
# usage: Test Ollama API connectivity and model functionality, run this before batch scanning

import requests
import json
from config import OLLAMA_API_URL, MODEL_NAME

def test_connection():
    # test 1: check Ollama connection
    print("Test 1: Checking Ollama connection...")
    try:
        response = requests.get("http://localhost:11434/api/tags", timeout=5)
        if response.status_code == 200:
            print("Ollama is running")
            return True
        else:
            print("Ollama response error")
            return False
    except requests.exceptions.ConnectionError:
        print("Unable to connect to Ollama, please ensure 'ollama serve' is running")
        return False
    except Exception as e:
        print(f"Error: {e}")
        return False

def test_model():
    # test 2: check if model is available
    print(f"\nTest 2: Checking model {MODEL_NAME}...")
    try:
        response = requests.get("http://localhost:11434/api/tags", timeout=5)
        data = response.json()
        models = [model['name'] for model in data.get('models', [])]
        
        if MODEL_NAME in models:
            print(f"Model {MODEL_NAME} is installed")
            return True
        else:
            print(f"Model {MODEL_NAME} not found")
            print(f"Available models: {', '.join(models)}")
            return False
    except Exception as e:
        print(f"Error: {e}")
        return False

def test_simple_query():
    # test 3: simple query test
    print("\nTest 3: Simple query test...")
    
    test_code = """
char buffer[10];
gets(buffer);
"""
    
    payload = {
        "model": MODEL_NAME,
        "prompt": f"Is there a buffer overflow in this code?\n{test_code}\nAnswer yes or no.",
        "stream": False
    }
    
    try:
        response = requests.post(OLLAMA_API_URL, json=payload, timeout=30)
        response.raise_for_status()
        result = response.json()
        
        print("API call successful.")
        print(f"Model response: {result['response'][:200]}...")
        return True
    except Exception as e:
        print(f"API call failed: {e}")
        return False

def test_vulnerability_detection():
    # test 4: check vulnerability detection
    print("\nTest 4: Checking vulnerability detection...")
    
    # sample vulnerable C code, can be replaced with any known vulnerable snippet
    vulnerable_code = """
#include <stdio.h>
#include <string.h>

void vulnerable_function(char *input) {
    char buffer[10];
    strcpy(buffer, input); 
    printf("%s\\n", buffer);
}

int main() {
    char large_input[100];
    gets(large_input);
    vulnerable_function(large_input);
    return 0;
}
"""
    
    payload = {
        "model": MODEL_NAME,
        # can customize prompt as needed
        "prompt": f"Analyze this C code for buffer overflow vulnerabilities:\n{vulnerable_code}",
        "stream": False
    }
    
    try:
        response = requests.post(OLLAMA_API_URL, json=payload, timeout=30)
        result = response.json()
        response_text = result['response'].lower()

        # Check if vulnerability is detected
        if any(keyword in response_text for keyword in ['buffer overflow', 'vulnerable', 'overflow']):
            print("Model successfully detected vulnerability")
            print(f"Model response snippet: {result['response'][:300]}...")
            return True
        else:
            print("Model did not explicitly identify vulnerability")
            print(f"Model response: {result['response']}")
            return False
    except Exception as e:
        print(f"Test failed: {e}")
        return False

def run_all_tests():
    """Run all tests"""
    print("=" * 60)
    print("Starting Ollama API tests")
    print("=" * 60)
    
    tests = [
        test_connection,
        test_model,
        test_simple_query,
        test_vulnerability_detection
    ]
    
    results = []
    for test in tests:
        results.append(test())
    
    print("\n" + "=" * 60)
    print(f"Test results: {sum(results)}/{len(results)} passed")
    print("=" * 60)
    
    if all(results):
        print("\nAll tests passed! You can start batch scanning.")
        return True
    else:
        print("\nSome tests failed, please check the configuration and try running the batch scan again.")
        return False

if __name__ == "__main__":
    run_all_tests()