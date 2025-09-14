#!/usr/bin/env python3
"""
Run the Streamlit app with API keys configured
"""

import os
import subprocess
import sys

def setup_environment():
    """Set up environment variables with API keys"""
    
    # Your Gemini API key
    os.environ['GEMINI_API_KEY'] = 'AIzaSyAlry5jmb1qqbFgvZztYImH6BC2-eFUpKU'
    
    # Your Helius API key
    os.environ['HELIUS_API_KEY'] = '327e16d6-4cdc-46a5-8b1a-9ed373e848d4'
    
    # CoinGecko API key (not needed - using Helius for prices)
    os.environ['COINGECKO_API_KEY'] = ''
    
    print("🔑 API Keys configured:")
    print(f"   ✅ Gemini API: {os.environ['GEMINI_API_KEY'][:20]}...")
    print(f"   ✅ Helius API: {os.environ['HELIUS_API_KEY'][:20]}...")
    print(f"   ⚪ CoinGecko API: Not needed (using Helius for prices)")

def run_streamlit():
    """Run the Streamlit app"""
    print("\n🚀 Starting Streamlit app...")
    
    try:
        # Run streamlit with the configured environment
        subprocess.run([sys.executable, '-m', 'streamlit', 'run', 'app.py'], 
                      env=os.environ.copy())
    except KeyboardInterrupt:
        print("\n👋 Streamlit app stopped.")
    except Exception as e:
        print(f"❌ Error running Streamlit: {e}")

if __name__ == "__main__":
    setup_environment()
    print("\n📝 Note: You'll need to get a Helius API key to fetch wallet data.")
    print("   Get it from: https://helius.xyz")
    print("\n🎯 The app will start but won't fetch real wallet data without Helius API key.")
    
    run_streamlit()
