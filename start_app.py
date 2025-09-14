#!/usr/bin/env python3
"""
Simple script to start the Solana Risk Dashboard
"""

import os
import sys
import subprocess

def main():
    # Set API keys
    os.environ['GEMINI_API_KEY'] = 'AIzaSyAlry5jmb1qqbFgvZztYImH6BC2-eFUpKU'
    os.environ['HELIUS_API_KEY'] = '327e16d6-4cdc-46a5-8b1a-9ed373e848d4'
    os.environ['COINGECKO_API_KEY'] = ''
    
    print("🚀 Starting Solana Risk Dashboard...")
    print("🔑 API Keys configured automatically")
    print("📱 Open http://localhost:8501 in your browser")
    print("=" * 50)
    
    # Get the path to the virtual environment's python
    venv_python = os.path.join(os.path.dirname(__file__), 'venv', 'bin', 'python')
    
    if not os.path.exists(venv_python):
        print("❌ Virtual environment not found!")
        print("Please run: python3 -m venv venv")
        print("Then: pip install -r requirements.txt")
        return
    
    # Run streamlit
    try:
        cmd = [venv_python, "-m", "streamlit", "run", "app.py", "--server.headless", "true"]
        subprocess.run(cmd, env=os.environ.copy())
    except KeyboardInterrupt:
        print("\n👋 Dashboard stopped.")
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    main()
