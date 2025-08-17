#!/usr/bin/env python3
"""
Test script to verify .env file loading
"""

import os
from config import ConfigLoader

def test_config_loading():
    """Test if configuration loading works properly"""
    print("Testing Configuration Loading")
    print("=" * 40)
    
    # Check if .env file exists
    env_file_exists = os.path.exists('.env')
    print(f".env file exists: {env_file_exists}")
    
    if env_file_exists:
        print(".env file contents:")
        with open('.env', 'r') as f:
            for line_num, line in enumerate(f, 1):
                if line.strip() and not line.strip().startswith('#'):
                    # Hide API keys for security
                    if 'API_KEY' in line:
                        key, value = line.split('=', 1)
                        masked_value = value[:10] + "..." if len(value) > 10 else "***"
                        print(f"  {line_num}: {key}={masked_value}")
                    else:
                        print(f"  {line_num}: {line.strip()}")
    else:
        print("No .env file found")
        print("Copy .env.example to .env and configure your settings")
        return
    
    print("\nTesting configuration loading...")
    try:
        config = ConfigLoader.load_from_env()
        print(f"Successfully loaded configuration!")
        print(f"   Provider: {config.llm.provider.value}")
        print(f"   Model: {config.llm.model}")
        print(f"   API Key: {'***' + config.llm.api_key[-4:] if config.llm.api_key and len(config.llm.api_key) > 4 else 'Not set'}")
        print(f"   Max Iterations: {config.max_iterations}")
        
    except Exception as e:
        print(f"ERROR: Configuration loading failed: {e}")
        print("\nTroubleshooting:")
        print("   - Make sure LLM_PROVIDER is set (openai, anthropic, google, groq, openrouter)")
        print("   - Make sure LLM_API_KEY is set with your actual API key")
        print("   - Check for typos in your .env file")

if __name__ == "__main__":
    test_config_loading()
