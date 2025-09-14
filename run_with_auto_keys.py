#!/usr/bin/env python3
"""
Run the Solana Risk Dashboard with API keys automatically configured
"""

import os
import subprocess
import sys

def main():
    """Run the dashboard with pre-configured API keys"""
    
    # Your API keys
    os.environ['GEMINI_API_KEY'] = 'AIzaSyAlry5jmb1qqbFgvZztYImH6BC2-eFUpKU'
    os.environ['HELIUS_API_KEY'] = '327e16d6-4cdc-46a5-8b1a-9ed373e848d4'
    os.environ['COINGECKO_API_KEY'] = ''
    
    print("🎯 Solana Risk Dashboard")
    print("=" * 40)
    print("🔑 API Keys automatically configured:")
    print(f"   ✅ Gemini API: {os.environ['GEMINI_API_KEY'][:20]}...")
    print(f"   ✅ Helius API: {os.environ['HELIUS_API_KEY'][:20]}...")
    print(f"   ⚪ CoinGecko API: Not needed")
    print("\n🚀 Starting dashboard...")
    print("📋 Open http://localhost:8501 in your browser")
    print("💡 Enter any Solana wallet address to analyze!")
    
    try:
        # Run streamlit
        subprocess.run([sys.executable, "-m", "streamlit", "run", "app.py"], 
                      env=os.environ.copy())
    except KeyboardInterrupt:
        print("\n👋 Dashboard stopped.")
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    main()
