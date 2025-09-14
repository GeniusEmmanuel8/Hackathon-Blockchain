#!/usr/bin/env python3
"""
Run the Solana Risk Dashboard
This script will work on GitHub Codespaces or any Python environment
"""

import os
import subprocess
import sys

def setup_environment():
    """Set up environment variables"""
    # You can set your API keys here or use environment variables
    if not os.getenv('GEMINI_API_KEY'):
        print("⚠️  GEMINI_API_KEY not found in environment variables")
        print("   You can set it in the sidebar of the app or as an environment variable")
    
    if not os.getenv('HELIUS_API_KEY'):
        print("⚠️  HELIUS_API_KEY not found in environment variables")
        print("   You can set it in the sidebar of the app or as an environment variable")
    
    print("🚀 Starting Solana Risk Dashboard...")
    print("📋 Open http://localhost:8501 in your browser")

def run_streamlit():
    """Run the Streamlit app"""
    try:
        subprocess.run([sys.executable, "-m", "streamlit", "run", "app.py", "--server.headless", "true"])
    except KeyboardInterrupt:
        print("\n👋 Dashboard stopped.")
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    setup_environment()
    run_streamlit()
