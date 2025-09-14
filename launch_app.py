#!/usr/bin/env python3
"""
Launch the Solana Risk Dashboard with all API keys configured
"""

import os
import subprocess
import sys

def setup_environment():
    """Set up environment variables with API keys"""
    
    # Your API keys
    os.environ['GEMINI_API_KEY'] = 'AIzaSyAlry5jmb1qqbFgvZztYImH6BC2-eFUpKU'
    os.environ['HELIUS_API_KEY'] = '327e16d6-4cdc-46a5-8b1a-9ed373e848d4'
    os.environ['COINGECKO_API_KEY'] = ''
    
    print("🔑 API Keys configured:")
    print(f"   ✅ Gemini API: {os.environ['GEMINI_API_KEY'][:20]}...")
    print(f"   ✅ Helius API: {os.environ['HELIUS_API_KEY'][:20]}...")
    print(f"   ⚪ CoinGecko API: Not needed")

def launch_streamlit():
    """Launch Streamlit using the virtual environment"""
    print("\n🚀 Launching Solana Risk Dashboard...")
    
    # Use the virtual environment's streamlit
    venv_streamlit = "./venv/bin/streamlit"
    
    try:
        # Run streamlit with the configured environment
        subprocess.run([venv_streamlit, 'run', 'app.py'], 
                      env=os.environ.copy())
    except KeyboardInterrupt:
        print("\n👋 Dashboard stopped.")
    except FileNotFoundError:
        print(f"❌ Streamlit not found at {venv_streamlit}")
        print("💡 Try running: ./venv/bin/python -m streamlit run app.py")
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    print("🎯 Solana Risk Dashboard Launcher")
    print("=" * 40)
    
    setup_environment()
    print("\n📋 Ready to analyze Solana wallets!")
    print("   • Enter any Solana wallet address")
    print("   • Get AI-powered risk insights")
    print("   • View portfolio visualizations")
    
    launch_streamlit()
