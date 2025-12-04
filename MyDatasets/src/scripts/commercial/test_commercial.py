# test_commercial.py
# Usage：Quickly test if commercial LLM APIs are configured correctly

from config_commercial import (
    CLAUDE_API_KEY, CHATGPT_API_KEY, GEMINI_API_KEY,
    MODEL_CONFIGS
)

def test_claude():
    """Test Claude API"""
    print("\nTesting Claude API...")
    
    if not CLAUDE_API_KEY:
        print("CLAUDE_API_KEY not set")
        return False
    
    try:
        import anthropic
        client = anthropic.Anthropic(api_key=CLAUDE_API_KEY)
        
        response = client.messages.create(
            model=MODEL_CONFIGS["claude"]["model_name"],
            max_tokens=100,
            messages=[
                {"role": "user", "content": "Say 'API test successful' if you can read this."}
            ]
        )
        
        result = response.content[0].text
        print(f"  Claude API is working")
        print(f"  Model: {MODEL_CONFIGS['claude']['model_name']}")
        print(f"  Response: {result[:50]}...")
        return True
        
    except ImportError:
        print("  anthropic library not installed")
        print("  Run: pip install anthropic")
        return False
    except Exception as e:
        print(f" Error: {e}")
        return False


def test_chatgpt():
    """Test ChatGPT API"""
    print("\nTesting ChatGPT API...")
    
    if not CHATGPT_API_KEY:
        print("CHATGPT_API_KEY not set")
        return False
    
    try:
        import openai
        client = openai.OpenAI(api_key=CHATGPT_API_KEY)
        
        response = client.chat.completions.create(
            model=MODEL_CONFIGS["chatgpt"]["model_name"],
            messages=[
                {"role": "user", "content": "Say 'API test successful' if you can read this."}
            ],
            max_tokens=100
        )
        
        result = response.choices[0].message.content
        print(f" ChatGPT API is working")
        print(f"  Model: {MODEL_CONFIGS['chatgpt']['model_name']}")
        print(f"  Response: {result[:50]}...")
        return True
        
    except ImportError:
        print("  openai library not installed")
        print("  Run: pip install openai")
        return False
    except Exception as e:
        print(f" Error: {e}")
        return False


def test_gemini():
    """Test Gemini API"""
    print("\nTesting Gemini API...")
    
    if not GEMINI_API_KEY:
        print("GEMINI_API_KEY not set")
        return False
    
    try:
        import google.generativeai as genai
        genai.configure(api_key=GEMINI_API_KEY)
        
        model = genai.GenerativeModel(MODEL_CONFIGS["gemini"]["model_name"])
        response = model.generate_content("Say 'API test successful' if you can read this.")
        
        result = response.text
        print(f" Gemini API is working")
        print(f"  Model: {MODEL_CONFIGS['gemini']['model_name']}")
        print(f"  Response: {result[:50]}...")
        return True
        
    except ImportError:
        print("  google-generativeai library not installed")
        print("  Run: pip install google-generativeai")
        return False
    except Exception as e:
        print(f" Error: {e}")
        return False


def main():
    print("=" * 60)
    print("Commercial LLM API Tester")
    print("=" * 60)
    
    tests = {
        "Claude": test_claude,
        "ChatGPT": test_chatgpt,
        "Gemini": test_gemini
    }
    
    results = {}
    for name, test_func in tests.items():
        results[name] = test_func()
    
    print("\n" + "=" * 60)
    print("Test Summary")
    print("=" * 60)
    
    for name, passed in results.items():
        status = "Available" if passed else "Unavailable"
        print(f"{name:15} {status}")
    
    success_count = sum(results.values())
    print(f"\nAvailable LLMs: {success_count}/{len(results)}")
    
    if success_count > 0:
        print("\nAt least one LLM is available, you can start scanning!")
    else:
        print("\nNo LLMs are available, please check the configuration")


if __name__ == "__main__":
    main()