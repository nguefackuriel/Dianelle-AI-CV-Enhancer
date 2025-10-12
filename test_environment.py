#!/usr/bin/env python3
"""
Simple test to verify the environment is working
"""

def test_imports():
    """Test all major imports"""
    print("🔍 Testing imports...")
    
    try:
        import streamlit as st
        print("✅ Streamlit imported successfully")
    except ImportError as e:
        print(f"❌ Streamlit import failed: {e}")
        return False
    
    try:
        import PyPDF2
        print("✅ PyPDF2 imported successfully")
    except ImportError as e:
        print(f"❌ PyPDF2 import failed: {e}")
    
    try:
        import requests
        print("✅ Requests imported successfully")
    except ImportError as e:
        print(f"❌ Requests import failed: {e}")
    
    try:
        import plotly
        print("✅ Plotly imported successfully")
    except ImportError as e:
        print(f"❌ Plotly import failed: {e}")
    
    try:
        import pandas as pd
        print("✅ Pandas imported successfully")
    except ImportError as e:
        print(f"❌ Pandas import failed: {e}")
    
    try:
        import nltk
        print("✅ NLTK imported successfully")
    except ImportError as e:
        print(f"❌ NLTK import failed: {e}")
    
    return True

def test_ollama_connection():
    """Test Ollama connection"""
    print("\n🔌 Testing Ollama connection...")
    
    try:
        import requests
        response = requests.get("http://localhost:11434/api/tags", timeout=5)
        if response.status_code == 200:
            print("✅ Ollama server is running and accessible")
            models = response.json().get('models', [])
            print(f"📋 Available models: {len(models)}")
            for model in models[:3]:  # Show first 3 models
                print(f"   - {model['name']}")
            return True
        else:
            print(f"❌ Ollama server responded with status: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Cannot connect to Ollama: {e}")
        return False

if __name__ == "__main__":
    print(" CV Enhancer Environment Test")
    print("=" * 40)
    
    imports_ok = test_imports()
    ollama_ok = test_ollama_connection()
    
    print("\n Test Results:")
    print("=" * 40)
    
    if imports_ok and ollama_ok:
        print(" All tests passed! Environment is ready.")
        print(" You can now run: streamlit run app.py")
    elif imports_ok:
        print("⚠️  Imports OK, but Ollama needs setup.")
        print(" Please ensure Ollama is running: ollama serve")
    else:
        print("❌ Some imports failed. Please check your Python environment.")
    
    print("\n Ready to meet Dianelle, your AI career assistant!")
